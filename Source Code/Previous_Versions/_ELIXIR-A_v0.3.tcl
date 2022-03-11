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
## 0.3 Add floating number of lists.

package provide elixir 0.3

namespace eval ::elixir:: {
	# namespace export Elixir
	variable w;
	variable t;
	variable v;
	variable pnum;
	variable p_current;
}

proc ::elixir::elixirgui {} {
	variable t;
	variable w;

	#if the gui exist
	if { [winfo exists .topgui]} {
	wm deiconify .topgui
	return
	}

	set t [toplevel ".topgui"]
	wm resizable $t 1 1
	wm geometry $t 640x640+300+300
	wm title $t "Enhanced Ligand Exploration and Interaction Recognition Algorithm"

	# frame $w.molone
	# grid [label $w.molone.molone1 -width 23 -text "Pharmacophore name:"] -row 0 -column 0 
	# grid [entry $w.molone.molone2 -width 20] -row 0 -column 1 
	# grid [label $w.molone.molone3 -width 8 -text "X"] -row 0 -column 2 
	# grid [label $w.molone.molone4 -width 8 -text "Y"] -row 0 -column 3 
	# grid [label $w.molone.molone5 -width 8 -text "Z"] -row 0 -column 4
	# # pack $w.molone -side top -padx 10 -pady 1 -expand 0 -fill x

	# frame $w.mols
	# grid [label $w.mols.nameoflistbox -width 25 -text "Type of the pharmacophore:"] -row 1 -column 0
	# grid [ttk::combobox $w.mols.listbox -width 18 -textvariable listbox \
	# 	 	-values [list Hydrophobic Armoatic HydrogenDonor HydeogenAcceptor Posititvelon Negativelon ExclusionSphere] -state readonly] \
	# 	 	-row 1 -column 1
	# grid [entry $w.mols.x1 -width 8 -textvariable molsx1] -row 1 -column 2
	# grid [entry $w.mols.y1 -width 8 -textvariable molsy1] -row 1 -column 3
	# grid [entry $w.mols.z1 -width 8 -textvariable molsz1] -row 1 -column 4

	# ttk::scrollbar $y.c.yscroll 
	# pack $y.c.yscroll -side right -fill y
	# set w $y.c
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
	pack $w.head.help -side left
	pack $w.head.list -side left
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
	grid [entry $w.mols$i.x1 -width 8 -textvariable molsx1$i] -row 1 -column 2
	grid [entry $w.mols$i.y1 -width 8 -textvariable molsy1$i] -row 1 -column 3
	grid [entry $w.mols$i.z1 -width 8 -textvariable molsz1$i] -row 1 -column 4
	grid [label $w.mols$i.tmp -text ""] -row 2
	#pack $w.molone$i $w.mols$i -side top -padx 5 -pady 0
	}
	pack $w.molone1 $w.mols1 -side top -padx 5 -pady 0

proc ::elixir::packmols {} \
{
	variable w
	variable pnum
	for {set i 1} {$i <= 20} {incr i} {
		pack forget $w.molone$i $w.mols$i
	}
	for {set i 1} {$i <= $pnum} {incr i} {
		pack $w.molone$i $w.mols$i -side top -padx 5 -pady 0
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

proc elixir_tk {} {
	::elixir::elixirgui
}