package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.udf



object Preprocessor {


  //Udf_country : si country=False prendre la valeur de currency,
  // sinon si country est une chaîne de caractères de taille autre que 2 remplacer par null,
  // et sinon laisser la valeur country actuelle.
  // On veut les résultat dans une nouvelle colonne “country2”.
  // StructField(country,StringType,true), StructField(currency,StringType,true)
  def udf_country = udf{(country: String, currency: String) =>
    if (country == "False")
      currency
    else if (country.length != 2)
      null
    else
    country
  }

  //Udf_currency: si currency.length != 3 currency prend la valeur null,
  // sinon laisser la valeur currency actuelle.
  // On veut les résultats dans une nouvelle colonne “currency2”.
  def udf_currency = udf{(currency:String) =>
    if (currency.length != 3)
      null
    else
      currency
  }



  def main(args: Array[String]): Unit = {


    // Des réglages optionels du job spark. Les réglages par défaut fonctionnent très bien pour ce TP
    // on vous donne un exemple de setting quand même
    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12"
    ))

    // Initialisation de la SparkSession qui est le point d'entrée vers Spark SQL (donne accès aux dataframes, aux RDD,
    // création de tables temporaires, etc et donc aux mécanismes de distribution des calculs.)
    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP_spark")
      .getOrCreate()

import spark.implicits._


    /*******************************************************************************
      *
      *       TP 2
      *
      *       - Charger un fichier csv dans un dataFrame
      *       - Pre-processing: cleaning, filters, feature engineering => filter, select, drop, na.fill, join, udf, distinct, count, describe, collect
      *       - Sauver le dataframe au format parquet
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/

    val df = spark.read.format("csv").option("header", "true").load("/data/Download/train_clean.csv")

    println("Number of rows:"+df.count())
    println("List of columns:"+df.columns)
    println("Schema:"+df.schema)
    println("First 10 rows:"+df.show(10))


    println("hello world ! from Preprocessor")

    //Change columns datatype backers_count|final_status
    //
    val df2 = df.withColumn("backers_count", $"backers_count".cast("Int") ).withColumn("final_status", $"final_status".cast("Int") )
    print(df2.schema)
    println("Schema:"+df2.schema)

    //Drop de la colonne disable_communication
    val df3= df2.drop($"disable_communication").drop($"backers_count").drop($"state_changed_at")

    //Traitement colonnes
    val df4 = df3.withColumn("country2",udf_country($"country",$"currency"))
      .withColumn("currency2",udf_currency($"currency"))
      //.withColumn("final_status",$"final_status".cast("Boolean"))


    //set to 0 if final_status !=1
    //val df5 = df4.filter()

    //print(df4.schema)


  }

}
