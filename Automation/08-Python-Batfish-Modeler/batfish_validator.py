from pybatfish.client.session import Session
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints
from pathlib import Path 
import os 
import sys 

SOURCE_IP="10.255.110.1"
DESTINATION_IP="10.255.111.3"
NETWORK_NAME="enterprise_network"
SNAPSHOT_NAME="proposed-snapshot"
START_PORT = '@enter(HQ-EDGE-1)'
def main():
	print(
			f"---- Starting Batfish Pre-Deployment ----"
		)
	
	snapshot_directory = (
			Path(__file__).resolve().parent / "snapshot"
		)
	if not (snapshot_directory / "configs").is_dir():
		print(
				f"ERROR: Could not find 'configs' folder"
			)
		return 1
	try: 
		bf = Session(host="localhost", port=9996)

		bf.set_network("enterprise_network")
		bf.init_snapshot(
				str(snapshot_directory),
				name="proposed-snapshot",
				overwrite=True
			)

		print(
				f"---- 1) Checking Snapshot Initialization Parsing Issues ----"
			)

		issues = bf.q.initIssues().answer().frame()

		if not issues.empty: 
			errors = issues[issues["Type"] == "ERROR"]
			if not errors.empty:
				print("ERROR during Configuration Parse")
				print(errors[['Node', 'Type', 'Details']].to_string(index=False))
				print("-" * 50)
				sys.exit(1)
		else: 
			print(
					f"No Parsing Issues Found"
				)
		validation_passed = True 

		print(f"\nTesting SSH: {SOURCE_IP} -> {DESTINATION_IP}:22")
		ssh_reachability = bf.q.reachability(
			pathConstraints=PathConstraints(startLocation=START_PORT),
				headers=HeaderConstraints(
						srcIps=SOURCE_IP,
						dstIps=DESTINATION_IP,
						ipProtocols=["TCP"],
						dstPorts="22"
					)).answer().frame()

		if not ssh_reachability.empty:
			print(
					f"PASS: SSH Flow is reachable in modeled network"
				)
		else: 
			print(
					f"FAIL: Device was not reachable in modeled network"
				)
			print(ssh_reachability.to_string(index=False))
			validation_passed = False

		print(f"\nTesting Telnet: {SOURCE_IP} -> {DESTINATION_IP}:23")
		telnet_reachability = bf.q.reachability(
				pathConstraints=PathConstraints(startLocation=START_PORT),
		headers=HeaderConstraints(
						srcIps=SOURCE_IP,
						dstIps=DESTINATION_IP,
						ipProtocols=["TCP"],
						dstPorts=23
					), actions="DENIED_IN").answer().frame()
		if not telnet_reachability.empty and "DENIED" in str(telnet_reachability['Traces'].values):
			print(
					f"PASS: Telnet was Successfully blocked in Modeled Network"
				)
		else: 
			print(
					f"FAIL: Telnet was reachable in the modeled network"
				)

		if validation_passed:
			print(
					f"#### All Batfish Reachability Test Passed ####"
				)
			sys.exit(0)
		else: 
			print(
				f"#### Batfish Validation Failed ###"
			)
			sys.exit(1)
	except Exception as e:
		print(f"Try/Exception: {str(e)}")
if __name__=="__main__":
	main()