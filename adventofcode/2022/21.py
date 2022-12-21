# Python Standard Library Imports
import operator
import re
import typing as T
from collections import deque
from dataclasses import dataclass

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (276156919469632, 3441198826073)
config.TEST_CASES = {
    '': (152, 301),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self):
        solver = Solver(self.data)
        solver.solve()
        answer = solver.values['root']
        return answer

    def solve2(self):
        solver = Solver(self.data)
        solver.solve2()
        answer = solver.values['humn']
        return answer


class Solver:
    """Solver for simple algebraic expression

    Inspiration: https://docs.sympy.org/latest/modules/solvers/solvers.html
    """

    @dataclass
    class Expression:
        VALUE_REGEX = re.compile(r'^(?P<symbol>\w+): (?P<value>\d+)$')
        EXPR_REGEX = re.compile(
            r'^(?P<symbol>\w+): (?P<operand1>\w+) (?P<op>[\+\-\*/]) (?P<operand2>\w+)$'
        )

        OPERATORS = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.floordiv,
        }

        INVERSE_OPERATORS = {
            '+': '-',
            '-': '+',
            '*': '/',
            '/': '*',
        }

        symbol: str
        value: T.Optional[int] = None
        op: T.Optional[str] = None
        operand1: T.Optional[str] = None
        operand2: T.Optional[str] = None

        @classmethod
        def from_raw(cls, raw_expression):
            if RE.match(cls.VALUE_REGEX, raw_expression):
                keys = ['symbol', 'value']
                transformers = [lambda x: x, lambda x: int(x)]
                expression = cls(
                    **{
                        key: transform(RE.m.group(key))
                        for (key, transform) in zip(keys, transformers)
                    }
                )
            elif RE.match(cls.EXPR_REGEX, raw_expression):
                keys = ['symbol', 'op', 'operand1', 'operand2']
                expression = cls(**{key: RE.m.group(key) for key in keys})
            else:
                raise Exception(f'Bad expression: {raw_expression}')

            return expression

        def __str__(self):
            if self.is_solved:
                s = f'{self.symbol}: {self.value}'
            else:
                s = f'{self.symbol}: {self.operand1} {self.op} {self.operand2}'
            return s

        @property
        def is_solved(self):
            return self.value is not None

        def evaluate(self, values):
            a = values.get(self.operand1)
            b = values.get(self.operand2)
            if a is not None and b is not None:
                self.value = self.OPERATORS[self.op](a, b)

            return self.value

        def is_solvable(self, values):
            """Determines whether this expression is solvable

            Returns True if at least 2 of 3 variables are known
            """
            a = values.get(self.operand1)
            b = values.get(self.operand2)
            c = values.get(self.symbol)
            is_solvable = (
                len(list(filter(lambda _: _ is not None, (a, b, c)))) >= 2
            )
            return is_solvable

        def re_express(self, values):
            """Given a solvable expression (at least 2 variables out of 3 are defined),
            rewrites the expression so that the unknown variable is on its own.
            """
            a = values.get(self.operand1)
            b = values.get(self.operand2)
            c = values.get(self.symbol)

            if a is None:
                new_expression = self.__class__(
                    symbol=self.operand1,
                    op=self.INVERSE_OPERATORS[self.op],
                    operand1=self.symbol,
                    operand2=self.operand2,
                )
            elif b is None:
                if self.op in ('+', '*'):
                    new_expression = self.__class__(
                        symbol=self.operand2,
                        op=self.INVERSE_OPERATORS[self.op],
                        operand1=self.symbol,
                        operand2=self.operand1,
                    )
                elif self.op in ('-', '/'):
                    new_expression = self.__class__(
                        symbol=self.operand2,
                        op=self.op,
                        operand1=self.operand1,
                        operand2=self.symbol,
                    )
                else:
                    raise Exception("C'est impossible!")
            else:
                raise Exception('Why did we get here, impossible case?')

            return new_expression

    def __init__(self, data):
        expressions = [
            self.Expression.from_raw(raw_expression) for raw_expression in data
        ]

        self.values = {
            expression.symbol: expression.value
            for expression in expressions
            if expression.is_solved
        }

        self.unsolved = deque(filter(lambda x: not x.is_solved, expressions))

    def solve(self):
        while len(self.unsolved) > 0:
            self.debug_unsolved()
            expression = self.unsolved.popleft()
            expression.evaluate(self.values)
            if expression.is_solved:
                self.values[expression.symbol] = expression.value
            elif expression.is_solvable(self.values):
                new_expression = expression.re_express(self.values)
                self.unsolved.append(new_expression)
            else:
                self.unsolved.append(expression)

    def solve2(self):
        # remove the value for 'humn'
        del self.values['humn']

        # rewrite the equation for 'humn'
        while self.unsolved[0].operand1 != 'humn':
            self.unsolved.rotate()
        if self.unsolved[0].operand1 == 'humn':
            old_expression = self.unsolved.popleft()
            new_expression = self.Expression(
                symbol='humn',
                op=self.Expression.INVERSE_OPERATORS[old_expression.op],
                operand1=old_expression.symbol,
                operand2=old_expression.operand2,
            )
            self.unsolved.append(new_expression)
        else:
            raise Exception('Unexpected')

        # rewrite the equation for 'root'
        while self.unsolved[0].symbol != 'root':
            self.unsolved.rotate()
        if self.unsolved[0].symbol == 'root':
            old_expression = self.unsolved.popleft()
            new_expression_a = self.Expression(
                symbol=old_expression.operand1,
                op='+',
                operand1='root',
                operand2=old_expression.operand2,
            )
            new_expression_b = self.Expression(
                symbol=old_expression.operand2,
                op='+',
                operand1=old_expression.operand1,
                operand2='root',
            )
            self.unsolved.append(new_expression_a)
            self.unsolved.append(new_expression_b)

            self.values['root'] = 0
        else:
            raise Exception('Unexpected')

        debug('Part 2: New Expressions')
        # finally, call the original solver
        self.solve()

    def debug_unsolved(self):
        if config.DEBUGGING:
            debug('-' * 20)
            for expr in self.unsolved:
                debug(str(expr))

            debug(self.values)
            debug('-' * 20)


if __name__ == '__main__':
    main()
