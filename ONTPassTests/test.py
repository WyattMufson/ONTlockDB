from ONTPassTests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaFixtureTest):

    def test_invalidFunction(self):

        output = Compiler.instance().load('%s/ONTPassDB/ONTPass.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['invalid', []], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)
