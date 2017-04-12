import unittest
import os

from csv_writer import CSVWriter
from pyspark.sql import SparkSession

INPUT_PATH = os.path.join(os.path.dirname(__file__), os.path.join("data", "test_input.csv"))
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), os.path.join("data", "test_output.csv"))

class CSVWriterTestCase(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(OUTPUT_PATH):
            os.remove(OUTPUT_PATH)

    def test__init__(self):
        writer = CSVWriter(INPUT_PATH, ";", "utf-8")
        self.assertEqual(writer.encoding, "utf-8", "Encoding should be utf-8")
        self.assertEqual(writer.sep, ";", "Separator should be ';'")
        self.assertEqual(writer.path, INPUT_PATH, "Path to file should be data/test_input.csv")


    def test_write(self):
        writer = CSVWriter(OUTPUT_PATH, ";", "utf-8")

        spark = SparkSession\
            .builder\
            .appName("LinesWriter")\
            .getOrCreate()

        dataframe = spark.read.csv(INPUT_PATH)

        writer.write(dataframe)
        spark.stop()

        self.assertTrue(os.path.exists(OUTPUT_PATH), "Output file 'test_output.csv' should be created")
        self.assertGreater(os.stat(OUTPUT_PATH).st_size, 0, "File should be not empty" )