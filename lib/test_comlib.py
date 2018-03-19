import comlib
import unittest
import json

class TestComlib(unittest.TestCase):
    
    def new_cmd(self, ver, t, v=True):
        ret = {}
        ret['version'] = ver
        ret['type'] = t
        ret['value'] = v
        return ret
    
    def helper_test(self, version, command):
        g = comlib.GameServer()
        cmd = self.new_cmd(version, command)
        resp = g.parseAction(cmd)
        return (g, json.loads(resp))

    def test_get_board(self):
        version = '0.3.1'        
        g, resp = self.helper_test(version, "get_board")

        # Test for existence of keys in response message
        self.assertTrue('version' in resp)
        self.assertTrue('response_type' in resp)
        self.assertTrue('value' in resp)

        # Test for right values in response
        self.assertEqual(resp['version'], version)
        self.assertEqual(resp['response_type'], 'board')

        # Check that the initial values of the board is only zeroes
        non_zeroes = g.getBoard().getNumberOfNonZeroesForEachRow()
        for row in non_zeroes:
            self.assertEqual(row, 0)

    def test_get_active_shape(self):
        return


if __name__ == '__main__':
    unittest.main()
        

    
    
    
