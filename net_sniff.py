import pyshark
import subprocess,os
val=input("Enter duration to capture: ")
out_file=raw_input("Enter file names: ")
print "\n"
cwd=os.getcwd()
out_filep=cwd+"/"+out_file+".pcap"
out_filex=cwd+"/"+out_file+".xml"
try:
	capture = pyshark.LiveCapture(interface='wlp4s0',output_file=out_filep)
	capture.sniff(timeout=val)
	print capture,"\n"
	#a=["tshark","-r",out_filep,"-T","psml",">",out_filex]
	#subprocess.call(a)
	os.system("tshark -r "+out_filep+" -T psml >  "+out_filex)
except:
	pass
print("\nCompleted")
