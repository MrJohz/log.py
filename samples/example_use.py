import log

logger = log.Logger()
logger.add_output("stdout")
logger.add_output("stderr", level=log.level("ERROR"))
logger.add_output("blue_logs.log", filter=lambda tag: tag == "blue")

logger.add_tags("green")

logger.log("Some small debug information about green.", level=log.DEBUG)
logger.log("Some small debug information about red and green.", level=log.DEBUG, tags=["red"])
logger.log("A blue error!", level=log.ERROR, tags='blue')

logger.clear_tags()

logger.log("This has no tags, and is on the default (INFO) level.")
logger.log("This has the blue tag, and is on the default level.", tags="blue")

logger.add_tags("green", "blue")

logger2 = logger.spawn()

logger2.clear_tags()

logger2.tags()
# ["green", "blue"]

logger2.clear_tags(force=True)
logger2.tags()
# []

logger.tags()
# ["green", "blue"]
logger.remove_tags("green")
logger.tags()
# ["blue"]

logger2 is logger
# False
logger.name
# "default"
logger2.name
# "default.default"

logger.spawn("sublogger").name
# default.sublogger

logger3 = log.Logger()
logger3 is logger
# False

logger4 = log.Logger("logger_name")
logger5 = log.Logger("logger_name")
logger4 is logger5
# True


