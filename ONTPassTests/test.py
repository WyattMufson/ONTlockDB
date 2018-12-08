from ONTPassTests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Prompt.Commands.BuildNRun import TestBuild
from neo.EventHub import events
from neo.SmartContract.SmartContractEvent import SmartContractEvent


class TestContract(BoaFixtureTest):

    @classmethod
    def setUpClass(cls):
        super(TestContract, cls).setUpClass()

        def on_notif(evt):
            print(evt)

        def on_log(evt):
            if evt.event_payload is not None:
                if evt.event_payload.ToJson() is not None:
                    val = evt.event_payload.ToJson()["value"]
                    print(val)

        events.on(SmartContractEvent.RUNTIME_NOTIFY, on_notif)
        events.on(SmartContractEvent.RUNTIME_LOG, on_log)

    def test_invalidFunction(self):
        output = Compiler.instance().load('%s/ONTPassDB/ONTPass.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['invalid', []], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

    def test_put_and_get(self):
        output = Compiler.instance().load('%s/ONTPassDB/ONTPass.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['put', [self.wallet_1_addr, "http://google.com", "password"]], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['get', [self.wallet_1_addr, "http://google.com"]], self.GetWallet1(), '07', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetString(), "password")
