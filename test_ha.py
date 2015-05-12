#!/usr/bin/env python 
# -*- coding: utf-8
import unittest
import parser_drbd

class TestDrbdParser(unittest.TestCase):
    def test_parse1(self):
        class ConnectorStub(object):
            def getDrbdLines(self):
                return ['version: 8.4.3 (api:1/proto:86-101)\n', 'srcversion: F97798065516C94BE0F27DC \n', '\n', ' 1: cs:Connected ro:Primary/Secondary ds:UpToDate/UpToDate C r-----\n', '    ns:5206108 nr:0 dw:5206108 dr:48757241 al:645 bm:0 lo:0 pe:0 ua:0 ap:0 ep:1 wo:d oos:0\n']
        p=parser_drbd.DrbdParser(1,ConnectorStub())
        p.parse()
        self.assertEqual(p.cs,'Connected')
        self.assertEqual(p.dr1,'Primary')
        self.assertEqual(p.dr2,'Secondary')
        self.assertEqual(p.ds1,'UpToDate')
        self.assertEqual(p.ds2,'UpToDate')
    def test_parse2(self):
        class ConnectorStub(object):
            def getDrbdLines(self):
                return ['version: 8.4.3 (api:1/proto:86-101)\n', 'srcversion: F97798065516C94BE0F27DC \n', '\n', ' 1: cs:Connected ro:Secondary/Secondary ds:UpToDate/UpToDate C r-----\n', '    ns:5206108 nr:0 dw:5206108 dr:48757241 al:645 bm:0 lo:0 pe:0 ua:0 ap:0 ep:1 wo:d oos:0\n']
        p=parser_drbd.DrbdParser(1,ConnectorStub())
        p.parse()
        self.assertEqual(p.cs,'Connected')
        self.assertEqual(p.dr1,'Secondary')
        self.assertEqual(p.dr2,'Secondary')
        self.assertEqual(p.ds1,'UpToDate')
        self.assertEqual(p.ds2,'UpToDate')


    def test_parse3(self):
        class ConnectorStub(object):
            def getDrbdLines(self):
                return ['version: 8.4.3 (api:1/proto:86-101)\n', 'srcversion: F97798065516C94BE0F27DC \n', '\n', '1: cs:WFConnection ro:Primary/Unknown ds:UpToDate/DUnknown C r-----\n', 'ns:5433228 nr:0 dw:5434240 dr:48876665 al:678 bm:0 lo:0 pe:0 ua:0 ap:0 ep:1 wo:d oos:884\n']
        p=parser_drbd.DrbdParser(1,ConnectorStub())
        p.parse()
        self.assertEqual(p.cs,'WFConnection')
        self.assertEqual(p.dr1,'Primary')
        self.assertEqual(p.dr2,'Unknown')
        self.assertEqual(p.ds1,'UpToDate')
        self.assertEqual(p.ds2,'DUnknown')

class TestHASlaveStrategy(unittest.TestCase):
    def test_both_ok_docker_down(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Primary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'demote_drbd')
    def test_both_ok_docker_up(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Primary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_slave_ok_docker_down(self):
        class ParserStub(object):
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Primary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_up')
    def test_slave_ok_docker_ok(self):
        class ParserStub(object):
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Primary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')

    def test_slave_secondary_disconnected_docker_down(self):
        class ParserStub(object):
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Secondary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'promote_drbd')

    def test_slave_secondary_disconnected_docker_up(self):
        class ParserStub(object):
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Secondary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_slave_secondary_connected_secondary_docker_down(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')

    def test_slave_secondary_connected_secondary_docker_up(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_slave_secondary_connected_primary_docker_up(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_slave_secondary_connected_primary_docker_down(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Primary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')

class TestHAMasterStrategy(unittest.TestCase):
    def test_both_ok_docker_down(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Primary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_up')
    def test_both_ok_docker_up(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Primary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')
    def test_master_ok_docker_down(self):
        class ParserStub(object):
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Primary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_up')
    def test_master_ok_docker_ok(self):
        class ParserStub(object):
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Primary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')

    def test_master_secondary_disconnected_docker_down(self):
        class ParserStub(object):
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Secondary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'promote_drbd')

    def test_master_secondary_disconnected_docker_up(self):
        class ParserStub(object):
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Secondary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_master_secondary_connected_secondary_docker_down(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'promote_drbd')

    def test_master_secondary_connected_secondary_docker_up(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_master_secondary_connected_primary_docker_up(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_master_secondary_connected_primary_docker_down(self):
        class ParserStub(object):
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Primary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(object):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')
#todo, implementar accions en funcio de strategy
#quan hi hagi accio desconeguda agent ha de fallar i enviar email

if __name__=='__main__':
    unittest.main()
