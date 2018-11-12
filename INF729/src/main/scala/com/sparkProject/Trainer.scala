package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.ml.feature._
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.evaluation.{BinaryClassificationEvaluator, MulticlassClassificationEvaluator}
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit}


object Trainer {

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12",
      "spark.driver.maxResultSize" -> "2g"
    ))

    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP_spark")
      .getOrCreate()


    /*******************************************************************************
      *
      *       TP 3
      *
      *       - lire le fichier sauvegarder précédemment
      *       - construire les Stages du pipeline, puis les assembler
      *       - trouver les meilleurs hyperparamètres pour l'entraînement du pipeline avec une grid-search
      *       - Sauvegarder le pipeline entraîné
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/


    //Lecture du dataset
    val rawdata = spark.read.parquet("/data/dev/prepared_trainingset")

    //1er stage: La première étape est séparer les textes en mots (ou tokens) avec un tokenizer.
    // Tokenizer le texte
    val tokenizer = new RegexTokenizer()
      .setPattern("\\W+")
      .setGaps(true)
      .setInputCol("text")
      .setOutputCol("tokens")


    //2e stage: On veut retirer les stop words pour ne pas encombrer le modèle
    // avec des mots qui ne véhiculent pas de sens. Créer le 2ème stage avec la classe StopWordsRemover.
    //Suppression des stop words qnglais
    val englishStopWords = StopWordsRemover.loadDefaultStopWords("english")
    val remover = new StopWordsRemover()
      .setInputCol("tokens")
      .setOutputCol("tokens_filtered")
      .setStopWords(englishStopWords)


    //3e stage: La partie TF de TF-IDF est faite avec la classe CountVectorizer.
    //vectorisation des tokens en couple
    val cv = new CountVectorizer()
      .setInputCol("tokens_filtered")
      .setOutputCol("rawFeatures")
      .setMinTF(2)
      .setMinDF(2)


    //4e stage: Trouvez la partie IDF.
    // On veut écrire l’output de cette étape dans une colonne “tfidf”.
    val idf = new IDF().setInputCol("rawFeatures").setOutputCol("tfidf")

    //5e stage: Convertir la variable catégorielle “country2” en quantités numériques.
    //On veut les résultats dans une colonne "country_indexed".
    //Index Country column
    val indexcol = new StringIndexer()
      .setInputCol("country2")
      .setOutputCol("country_indexed")

    //val indexed1 = indexer_col.transform(rescaledData)

    //6e stage: Convertir la variable catégorielle “currency2” en quantités numériques.
    //On veut les résultats dans une colonne "currency_indexed".
    //Index Currency column
    val indexcurr = new StringIndexer()
      .setInputCol("currency2")
      .setOutputCol("currency_indexed")

    //7e stage & 8e stage: transformer ces deux catégories avec un “one-hot encoder”.
    //OneHotEncoder : maps a column of category indices to a column of binary vectors
    val encoder1 = new OneHotEncoder()
      .setInputCol("country_indexed")
      .setOutputCol("countryVec")


    //OneHotEncoder : maps a column of category indices to a column of binary vectors
    val encoder2 = new OneHotEncoder()
      .setInputCol("currency_indexed")
      .setOutputCol("currencyVec")


    // 9e stage: Assembler les features "tfidf", "days_campaign", "hours_prepa",
    // "goal", "country_indexed", "currency_indexed"  dans une seule colonne “features”.
    val vectorAssembler = new VectorAssembler()
      .setInputCols(Array("tfidf", "days_campaign", "hours_prepa",
      "goal","countryVec","currencyVec"))
      .setOutputCol("features")


    //On assemble le pipeline de Transformation
    val transformationPipeline = new Pipeline()
      .setStages(Array(tokenizer,remover,cv,idf,indexcol,indexcurr,encoder1,encoder2,vectorAssembler))
    //Et on le lance
    val fittedPipeline = transformationPipeline.fit(rawdata)
    val transformedTraining = fittedPipeline.transform(rawdata)

    //On splitte la data en 2 jeu de tests et training
    val Array(train, test) = transformedTraining.randomSplit(Array(0.9, 0.1), seed = 12345)

    //On va tester une régression
    val lr = new LogisticRegression()
      .setElasticNetParam(0.0)
      .setFitIntercept(true)
      .setFeaturesCol("features")
      .setLabelCol("final_status")
      .setStandardization(true)
      .setPredictionCol("predictions")
      .setRawPredictionCol("raw_predictions")
      .setThresholds(Array(0.7, 0.3))
      .setTol(1.0e-6)
      .setMaxIter(300)

    //On ajoute à la pipeline de regression
    val Lrpipeline = new Pipeline().setStages(Array(lr))


    val params = new ParamGridBuilder()
      .addGrid(lr.regParam, Array(1.0e-8, 1.0e-6, 1.0e-4, 1.0e-2))
      .addGrid(cv.minDF, Array(55.0, 75.0, 95.0))
      .build()


    val evaluator = new MulticlassClassificationEvaluator()
      .setLabelCol("final_status")
      .setPredictionCol("predictions")
      .setMetricName("f1")



    //On prépare la crossvalidation/fitting sur le dataset de train
    val tvs = new TrainValidationSplit()
      .setTrainRatio(0.75)
      .setEstimatorParamMaps(params)
      .setEstimator(Lrpipeline)
      .setEvaluator(evaluator)

    //On fitte le dataset de training
    val tvsFitted = tvs.fit(train)
    //On effectue les predictions
    val df_WithPredictions = tvsFitted.transform(test)

    //Score de prediction du modèle
    val f1Score = evaluator.evaluate(df_WithPredictions)
    println("f1score : " + f1Score)

    //Visualisation des résultats de la prédiction
    df_WithPredictions.groupBy("final_status", "predictions").count.show()

  }
}
