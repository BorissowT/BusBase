from db.models import session
from db.models import Station


results = session.query(Station).all()


list = list(map(lambda elem: elem.Title, results))

print(list)