headers = {
    "json": {"Content-Type": "application/json"},
    "text": {"Content-Type": "text/html; charset=UTF-8"},
}


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d
