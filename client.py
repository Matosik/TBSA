import server
from consolemenu import ConsoleMenu, prompt_utils, Screen
from consolemenu.items import FunctionItem
import logging
import chord
from json import dumps
logging.basicConfig(level="INFO")


def create_network():
    server.start()
    server.node.network_create()


def connect_client():
    server.start()

    test_prompt = prompt_utils.PromptUtils(Screen())
    id_to = test_prompt.input("Enter the connection id: ").input_string

    logging.info(f"Connecting to #{id_to} ...")
    server.node.network_join(int(id_to))
    test_prompt.enter_to_continue()


def show_fingers():
    test_prompt = prompt_utils.PromptUtils(Screen())
    fingers = server.node.finger
    print(dumps(fingers, indent=4, ensure_ascii=False))
    test_prompt.enter_to_continue()


def recalc_fingers():
    test_prompt = prompt_utils.PromptUtils(Screen())
    server.node.find_fingers()
    test_prompt.enter_to_continue()


if __name__ == "__main__":
    main_prompt = prompt_utils.PromptUtils(Screen())
    id = main_prompt.input("Enter your id: ").input_string
    server.node = chord.ChordNode(int(id))

    menu = ConsoleMenu("P2P client")
    join_item = FunctionItem("Join network", connect_client)
    create_item = FunctionItem("Create network", create_network)
    show_item = FunctionItem("Print fingers table", show_fingers)
    recalc_item = FunctionItem("Recalc fingers table", recalc_fingers)
    menu.append_item(join_item)
    menu.append_item(create_item)
    menu.append_item(show_item)
    menu.append_item(recalc_item)
    menu.show()

    logging.info("Closing client...")
    server.exit_flag = True