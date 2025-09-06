#hotif (instr(wingetprocessname("A"),"empire",0))
F1:: {
wingetpos &x,&y,&w,&h,"A"
if (h=768){
click 1300,5
send("{up 4}")
send("{enter}")
click 420,500
click 590,550
	} else {
click 1907,9
send("{up 4}")
send("{enter}")
click 687,581
click 853,703
	}
}
`::8
8::`
q::9
9::q
z::0
0::z
p::w
w::p
capslock::
{
send("^8")
}
#hotif
#hotif (instr(wingetprocessname("A"),"gplay",0))
#maxthreadsperhotkey 2
on:=false
F1:: {
	global on
	on:=!on
	WinGetPos &X, &Y,,, "A"
	while on {
		click x+410, y+270
		sleep(1000)
		click x+410, y+390
		sleep(1000)
	}
return
}
#hotif