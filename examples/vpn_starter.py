from anon_starter import Anon

anon = Anon()

try:
    anon.start_vpn("fr")
    resp = anon.socks.get("http://ip-api.com/json")
    print(resp.text)
finally:
    anon.stop_vpn()
