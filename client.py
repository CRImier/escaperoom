import jsonrpclib
server = jsonrpclib.Server('http://localhost:8070')
server.start_game()

"""actions = {
"Start game":server.start_game,
"Stop game":server.stop_game,
"Get active steps":server.get_active_steps,
"Get steps":server.get_steps,
"Finish step":server.finish_step,
"Stress test":server.stress_test,

}
"""


