from db.db_settings import connection
from db.db_settings import engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Administrator = Base.classes.administrator
Bus = Base.classes.bus
DayReport = Base.classes.dayreport
Department = Base.classes.department
Driver = Base.classes.driver
DriverReport = Base.classes.driverreport
Organisation = Base.classes.organisation
Route = Base.classes.route
Ticketsman = Base.classes.ticketsman
TicketsmanReport = Base.classes.ticketsmanreport
Train = Base.classes.train
VehicleBase = Base.classes.vehiclebase


session = Session(engine)

