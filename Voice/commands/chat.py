on_keywords = ["enable", "enabled", "on"]
off_keywords = ["disable", "disabled", "off"]
toggle_keywords = ["toggle", "switch"]

def chat(args, vars):
    vars = vars

    if args[0] in on_keywords:
        vars.chatting = True

    if args[0] in off_keywords:
        vars.chatting = False

    if args[0] in toggle_keywords:
        vars.chatting = not vars.chatting

    return vars


def chatting(args, vars):
    vars = vars

    if args[0] in on_keywords:
        vars.chatting = True

    if args[0] in off_keywords:
        vars.chatting = False

    if args[0] in toggle_keywords:
        vars.chatting = not vars.chatting

    return vars

