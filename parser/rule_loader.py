from parser.rule_parser import RuleParser
CONSEQUENT_NODE = 1
FIRST_CONS = 0

def load_rules_from_files(rule_files):
    document_node = _parse_rules_file(rule_files)
    rules_dict = {}
    for if_then_node in document_node.children:
        parameter = if_then_node.children[CONSEQUENT_NODE].children[FIRST_CONS].param.name
        if parameter in rules_dict:
            rules_dict[parameter].append(if_then_node)
        else:
            rules_dict[parameter] = [if_then_node]
    return rules_dict


def _parse_rules_file(file):
    lines = (line.rstrip('\n') for line in open(file))
    rules = '\n'.join(lines)
    rule_parser = RuleParser(rules)
    return rule_parser.get_document_node()