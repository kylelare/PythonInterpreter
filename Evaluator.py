import traceback
from Parser import BinaryOperatorStatementNode, ExpressionNode


class PythonEvaluator:
    def __init__(self, ast=None):
        self.ast = ast
        self.variables = {}
        self.eval_ast()

    def eval_ast(self):
        print("evaluating AST:", self.ast)

        results = []
        for node in self.ast:
            if isinstance(node, BinaryOperatorStatementNode):
                self.handle_assignment(node)
            elif isinstance(node, ExpressionNode):
                result = self.evaluate_expression(node)
                results.append(result)

        print("Current variable evals:", self.variables)
        print("Evaluation results:", results)

    def handle_assignment(self, node):
        # Assuming right side is always a literal value or a string (for simplicity)
        # strip +- to make isdigit work for numbers including positive/negative symbol
        value = int(node.right) if node.right.strip('+-').isdigit() else node.right.strip('"')
        self.variables[node.left] = value

    def evaluate_expression(self, node):
        # print(self.variables)
        left = self.variables.get(node.left, node.left.strip("'"))
        right = self.variables.get(node.right, node.right.strip("'"))

        # convert digits to ints here
        if isinstance(left, str):
            # strip +- to make isdigit work for numbers including positive/negative symbol
            if left.strip('+-').isdigit():
                left = int(left)
        if isinstance(right, str):
            # strip +- to make isdigit work for numbers including positive/negative symbol
            if right.strip('+-').isdigit():
                right = int(right)

        try:
            # Todo build a dictionary for this instead of repeated ifs
            if node.operator == 'in':
                return left in right
            elif node.operator == '-':
                return left - right
            elif node.operator == '+':
                return left + right
            elif node.operator == "*":
                return left * right
            elif node.operator == "/":
                return left / right
            elif node.operator == "%":
                return left % right
            elif node.operator == "==":
                return left == right
            elif node.operator == "!=":
                return left != right
            elif node.operator == '>=':
                return left >= right
            elif node.operator == "<=":
                return left <= right
            else:
                raise ValueError(f"Unsupported operator: {node.operator}")
        except TypeError:
            traceback.print_exc()
