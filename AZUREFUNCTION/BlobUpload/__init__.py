import logging
import azure.functions as func


def main(inputBlob: func.InputStream, outputBlob: func.Out[func.InputStream]):
    logging.info(f'Blob {inputBlob.name} was successfully copied')
    outputBlob.set(inputBlob)
