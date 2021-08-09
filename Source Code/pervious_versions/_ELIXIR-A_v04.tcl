##
## ELIXIR-A
##
## A script to add two cluster of pharmacophores into one cluster
##
## The algorithm is copyrighted by Dr. Sandun Fernando
## 
## Script Author: Haoqi Wang
##
## Date: 09/25/2018
##
## Script name: ELIXIR-A.tcl

## Update history:
## 0.2 Using loop function for multiple pharmacophores.
## 0.3 Add floating number of pharmacophore lists.
## 0.4 Add paired pharmacophore lists.

package provide elixir 0.4
variable ELIXIRDIR

namespace eval ::elixir:: {
	# namespace export Elixir
	variable w;
	variable t;
	variable v;
	variable pnum;
	variable p_current "1st";
	variable pnum2;
	variable molsx11 0.000
	variable molsx12 0.000
	variable molsx13 0.000
	variable molsx14 0.000
	variable molsx15 0.000
	variable molsx16 0.000
	variable molsx17 0.000
	variable molsx18 0.000
	variable molsx19 0.000
	variable molsx110 0.000
	variable molsx111 0.000
	variable molsx112 0.000
	variable molsx113 0.000
	variable molsx114 0.000
	variable molsx115 0.000
	variable molsx116 0.000
	variable molsx117 0.000
	variable molsx118 0.000
	variable molsx119 0.000
	variable molsx120 0.000
	variable molsy11 0.000
	variable molsy12 0.000
	variable molsy13 0.000
	variable molsy14 0.000
	variable molsy15 0.000
	variable molsy16 0.000
	variable molsy17 0.000
	variable molsy18 0.000
	variable molsy19 0.000
	variable molsy110 0.000
	variable molsy111 0.000
	variable molsy112 0.000
	variable molsy113 0.000
	variable molsy114 0.000
	variable molsy115 0.000
	variable molsy116 0.000
	variable molsy117 0.000
	variable molsy118 0.000
	variable molsy119 0.000
	variable molsy120 0.000
	variable molsz11 0.000
	variable molsz12 0.000
	variable molsz13 0.000
	variable molsz14 0.000
	variable molsz15 0.000
	variable molsz16 0.000
	variable molsz17 0.000
	variable molsz18 0.000
	variable molsz19 0.000
	variable molsz110 0.000
	variable molsz111 0.000
	variable molsz112 0.000
	variable molsz113 0.000
	variable molsz114 0.000
	variable molsz115 0.000
	variable molsz116 0.000
	variable molsz117 0.000
	variable molsz118 0.000
	variable molsz119 0.000
	variable molsz120 0.000
	variable molsx21 0.000
	variable molsx22 0.000
	variable molsx23 0.000
	variable molsx24 0.000
	variable molsx25 0.000
	variable molsx26 0.000
	variable molsx27 0.000
	variable molsx28 0.000
	variable molsx29 0.000
	variable molsx210 0.000
	variable molsx211 0.000
	variable molsx212 0.000
	variable molsx213 0.000
	variable molsx214 0.000
	variable molsx215 0.000
	variable molsx216 0.000
	variable molsx217 0.000
	variable molsx218 0.000
	variable molsx219 0.000
	variable molsx220 0.000
	variable molsy21 0.000
	variable molsy22 0.000
	variable molsy23 0.000
	variable molsy24 0.000
	variable molsy25 0.000
	variable molsy26 0.000
	variable molsy27 0.000
	variable molsy28 0.000
	variable molsy29 0.000
	variable molsy210 0.000
	variable molsy211 0.000
	variable molsy212 0.000
	variable molsy213 0.000
	variable molsy214 0.000
	variable molsy215 0.000
	variable molsy216 0.000
	variable molsy217 0.000
	variable molsy218 0.000
	variable molsy219 0.000
	variable molsy220 0.000
	variable molsz21 0.000
	variable molsz22 0.000
	variable molsz23 0.000
	variable molsz24 0.000
	variable molsz25 0.000
	variable molsz26 0.000
	variable molsz27 0.000
	variable molsz28 0.000
	variable molsz29 0.000
	variable molsz210 0.000
	variable molsz211 0.000
	variable molsz212 0.000
	variable molsz213 0.000
	variable molsz214 0.000
	variable molsz215 0.000
	variable molsz216 0.000
	variable molsz217 0.000
	variable molsz218 0.000
	variable molsz219 0.000
	variable molsz220 0.000
}

proc ::elixir::elixirgui {} {
	variable t;
	variable w;
	variable v;


	#if the gui exist
	if { [winfo exists .topgui]} {
	wm deiconify .topgui
	return
	}

	set t [toplevel ".topgui"]
	wm resizable $t 1 1
	wm geometry $t 640x640+300+300
	wm title $t "Enhanced Ligand Exploration and Interaction Recognition Algorithm"

	#pharmocheore selection
	frame $t.phselect
	label $t.phselect.description -text \
	"\nELIXIR-A is designed to combine two ligands (pharmacophores) simultaneously toward\n a \
	receptor for further Pharmacophore-based Virtual Screening.\n"
	label $t.phselect.label01 -text "The pharmacophores in the"
	tk_optionMenu $t.phselect.list ::elixir::p_current "1st"
	$t.phselect.list.menu delete 0
	$t.phselect.list.menu add radiobutton -label "1st" \
		-variable ::elixir::p_current \
		-command ::elixir::changepcurrent
	$t.phselect.list.menu add radiobutton -label "2nd" \
		-variable ::elixir::p_current \
		-command ::elixir::changepcurrent
	label $t.phselect.label02 -text "cluster"

	pack $t.phselect 
	pack $t.phselect.description -side top -padx 10 -expand 1
	pack $t.phselect.label01 $t.phselect.list $t.phselect.label02 -side left -fill x
	set w [frame $t.pharm1]
	frame $w.head
	label $w.head.help -text "The number of the pharmacophores in the 1st molecule."
	tk_optionMenu $w.head.list ::elixir::pnum 1
	$w.head.list.menu delete 0
	for {set i 1} {$i <= 7} {incr i} {
		$w.head.list.menu add radiobutton -label $i \
		-variable ::elixir::pnum \
		-command ::elixir::packmols
	}
	pack $w
	pack $w.head.help -side left -padx 0
	pack $w.head.list -side left -padx 0
	pack $w.head -side top -pady 2 -fill x
	# pack $w.head.list -side top -fill x

	for {set i 1} {$i <= 20} {incr i} {
	frame $w.molone$i
	grid [label $w.molone$i.molone1 -width 23 -text "Pharmacophore$i:"] -row 0 -column 0 
	grid [entry $w.molone$i.molone2 -width 20] -row 0 -column 1 
	grid [label $w.molone$i.molone3 -width 8 -text "X"] -row 0 -column 2 
	grid [label $w.molone$i.molone4 -width 8 -text "Y"] -row 0 -column 3 
	grid [label $w.molone$i.molone5 -width 8 -text "Z"] -row 0 -column 4
	# pack $w.molone -side top -padx 10 -pady 1 -expand 0 -fill x

	frame $w.mols$i
	grid [label $w.mols$i.nameoflistbox -width 25 -text "Type of the pharmacophore:"] -row 1 -column 0
	grid [ttk::combobox $w.mols$i.listbox -width 18 -textvariable listbox$i \
		 	-values [list Hydrophobic Armoatic HydrogenDonor HydeogenAcceptor Posititvelon Negativelon ExclusionSphere] -state readonly] \
		 	-row 1 -column 1
	grid [entry $w.mols$i.x1 -width 8 -textvariable ::elixir::molsx1$i] -row 1 -column 2
	grid [entry $w.mols$i.y1 -width 8 -textvariable ::elixir::molsy1$i] -row 1 -column 3
	grid [entry $w.mols$i.z1 -width 8 -textvariable ::elixir::molsz1$i] -row 1 -column 4
	grid [label $w.mols$i.tmp -text ""] -row 2
	#pack $w.molone$i $w.mols$i -side top -padx 5 -pady 0
	}
	pack $w.molone1 $w.mols1 -side top -padx 0 -pady 0

	
	#The GUI for the second pharmocophore.
	set v [frame $t.pharm2]
	frame $v.head
	label $v.head.help -text "The number of the pharmacophores in the 2nd molecule."
	tk_optionMenu $v.head.list ::elixir::pnum2 1
	$v.head.list.menu delete 0
	for {set i 1} {$i <= 7} {incr i} {
		$v.head.list.menu add radiobutton -label $i \
		-variable ::elixir::pnum2 \
		-command ::elixir::packmols2
	}
	pack $v.head.help -side left -padx 0
	pack $v.head.list -side left -padx 0
	pack $v.head -side top -pady 2 -fill x
	# pack $v.head.list -side top -fill x

	for {set i 1} {$i <= 20} {incr i} {
	frame $v.molone$i
	grid [label $v.molone$i.molone1 -width 23 -text "Pharmacophore$i:"] -row 0 -column 0 
	grid [entry $v.molone$i.molone2 -width 20] -row 0 -column 1 
	grid [label $v.molone$i.molone3 -width 8 -text "X"] -row 0 -column 2 
	grid [label $v.molone$i.molone4 -width 8 -text "Y"] -row 0 -column 3 
	grid [label $v.molone$i.molone5 -width 8 -text "Z"] -row 0 -column 4
	# pack $v.molone -side top -padx 10 -pady 1 -expand 0 -fill x

	frame $v.mols$i
	grid [label $v.mols$i.nameoflistbox -width 25 -text "Type of the pharmacophore:"] -row 1 -column 0
	grid [ttk::combobox $v.mols$i.listbox -width 18 -textvariable listbox2$i \
		 	-values [list Hydrophobic Armoatic HydrogenDonor HydeogenAcceptor Posititvelon Negativelon ExclusionSphere] -state readonly] \
		 	-row 1 -column 1
	grid [entry $v.mols$i.x1 -width 8 -textvariable ::elixir::molsx2$i] -row 1 -column 2
	grid [entry $v.mols$i.y1 -width 8 -textvariable ::elixir::molsy2$i] -row 1 -column 3
	grid [entry $v.mols$i.z1 -width 8 -textvariable ::elixir::molsz2$i] -row 1 -column 4
	grid [label $v.mols$i.tmp -text ""] -row 2
	#pack $v.molone$i $v.mols$i -side top -padx 5 -pady 0
	}
	pack $v.molone1 $v.mols1 -side top -padx 0 -pady 0

proc ::elixir::packmols {} \
{
	variable w
	variable pnum
	for {set i 1} {$i <= 20} {incr i} {
		pack forget $w.molone$i $w.mols$i
	}
	for {set i 1} {$i <= $pnum} {incr i} {
		pack $w.molone$i $w.mols$i -side top -padx 0 -pady 0
	}
}
proc ::elixir::packmols2 {} \
{
	variable v
	variable pnum2
	for {set i 1} {$i <= 20} {incr i} {
		pack forget $v.molone$i $v.mols$i
	}
	for {set i 1} {$i <= $pnum2} {incr i} {
		pack $v.molone$i $v.mols$i -side top -padx 0 -pady 0
	}
}

proc changepcurrent {} \
{
	variable p_current
	variable w
	variable t
	variable v
	if {$p_current=="1st"} {
		pack forget $w $v
		pack $w
	} else {
		pack forget $w $v
		pack $v
	}

}

	#scrollbar
	# $w configure -scrollregion [$w bbox all]


	# grid [ttk::combobox $w.mols.listbox -values [list USA Canada Australia] -state readonly]
	#bind .atom1 <<ComboboxSelected>> { script }
	

	# set $w.mols.listbox $w.mols.listbox.current(3) 
	#set the default for combobox

	return $t
}

#ELIXIR::elixirgui

proc ::elixir::call_python {} {
# set output [exec python [file join $::env(ELIXIRDIR) "hello.py"]]
#test on 
set output [exec python "hello.py" [list $::elixir::molsx11 $::elixir::molsx12 $::elixir::molsx13 \
	$::elixir::molsx11 $::elixir::molsx12 $::elixir::molsx13 \
	$::elixir::molsx11 $::elixir::molsx12 $::elixir::molsx13 \
	$::elixir::molsx11 $::elixir::molsx12 $::elixir::molsx13 \
	]]
puts $output
# puts [list $::elixir::molsx11 $::elixir::molsx12 $::elixir::molsx13 \
# $::elixir::molsx11 $::elixir::molsx12 $::elixir::molsx13 \
# $::elixir::molsx11 $::elixir::molsx12 $::elixir::molsx13 \
# $::elixir::molsx11 $::elixir::molsx12 $::elixir::molsx13 \
# ]
}

proc elixir_tk {} {
	::elixir::elixirgui
	
}