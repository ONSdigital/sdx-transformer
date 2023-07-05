from sdx_gcp import Request, Flask, TX_ID


def transform(req: Request, tx_id: TX_ID):
    zip_file = ""
    return Flask.send_file(zip_file, mimetype='application/zip', etag=False)
