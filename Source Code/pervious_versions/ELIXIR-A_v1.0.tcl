##
## ELIXIR-A
##
## A script to add two cluster of pharmacophores into one cluster
##
## The algorithm is copyrighted by Dr. Sandun Fernando
## 
## Script Author: Haoqi Wang
##
## Date: 07/25/2021
##
## Script name: ELIXIR-A.tcl

## Update history:
## 0.2 Using loop function for multiple pharmacophores.
## 0.3 Add floating number of pharmacophore lists.
## 0.4 Add paired pharmacophore lists.
## 0.5 Develop the interact with the algorithm in python 09/30/2018
## 0.6 Update the appearance.
## 0.7 Fix mirror bugs. 
## 0.8 Fix mirror bugs.
## 0.9 Update on the JSON output
## 1.0 Fix bugs

package provide elixir 1.0
package require tile
variable ELIXIRDIR

namespace eval ::elixir:: {
	# namespace export Elixir
	variable w;
	variable t;
	variable v;
	variable ph1id;
	variable ph2id;
	# variable pnum;
	variable p_current "1st";
	# variable pnum2;
	variable llbox;
	variable ph1x 0.000;
	variable ph1y 0.000;
	variable ph1z 0.000;
	variable ph1type "Default";
	variable ph1vn "Default";
	variable ph1data [list]
	variable ph1indexs [list [lrepeat 50 0]];
	variable ph1index 0;
	variable ph2x 0.000;
	variable ph2y 0.000;
	variable ph2z 0.000;
	variable ph2type "Default";
	variable ph2vn "Default2";
	variable ph2data [list]
	variable ph2indexs [list [lrepeat 50 0]];
	variable ph2index 0;
	variable outputfolder "";
	variable logout 1;
	variable jsonout 0;
	variable numiterations 100;
	variable threshold 100;
}

proc ::elixir::elixirgui {} {
	variable t;
	variable w;
	variable v;

	#if the gui exists.
	if { [winfo exists .topgui]} {
	wm deiconify .topgui
	return
	}

	set t [toplevel ".topgui"]
	wm resizable $t 1 1
	wm geometry $t 640x860+150+50
	wm title $t "Enhanced Ligand Exploration and Interaction Recognition Algorithm"

	#description
	frame $t.topside
	label $t.topside.description -text \
	"\nELIXIR-A is designed to combine two ligands (pharmacophores) simultaneously toward\n a \
	receptor for further Pharmacophore-based Virtual Screening.\n"
	pack $t.topside.description
	pack $t.topside -side top -fill both

	#pharmocheore number 1
	frame $t.ph1
	label $t.ph1.label01 -text "The First pharmacophore cluster."
	label $t.ph1.label02 -text "Variable name"
	label $t.ph1.label03 -text "Pharmacophore type"
	label $t.ph1.labelx -width 8 -text "X"
	label $t.ph1.labely -width 8 -text "Y"
	label $t.ph1.labelz -width 8 -text "Z"
	entry $t.ph1.entry1 -width 12 -textvariable ::elixir::ph1vn 
	entry $t.ph1.entryx -textvariable ::elixir::ph1x -width 8
	entry $t.ph1.entryy -textvariable ::elixir::ph1y -width 8
	entry $t.ph1.entryz -textvariable ::elixir::ph1z -width 8
	button $t.ph1.op -text "Import from pdb" -command ::elixir::openprotein
	button $t.ph1.ad -text Add -command ::elixir::ph1add -width 5
	button $t.ph1.ck -text Check -command ::elixir::checkstatus
	button $t.ph1.dl -text Delete -command ::elixir::ph1del

	#geometry box
	grid $t.ph1.label01 -row 1 -columnspan 5
	grid $t.ph1.label02 -row 2 -column 1
	grid $t.ph1.entry1  -row 2 -column 2
	grid $t.ph1.labelx -row 2 -column 3
	grid $t.ph1.labely -row 2 -column 4
	grid $t.ph1.labelz -row 2 -column 5
	grid $t.ph1.label03 -row 3 -column 1
	grid [ttk::combobox $t.ph1.listbox1 -width 18 -textvariable ::elixir::ph1type \
	 	-values [list Default Hydrophobic Aromatic HydrogenDonor HydeogenAcceptor Positivelon Negativelon ExclusionSphere] -state readonly] \
	 	-row 3 -column 2
	grid $t.ph1.entryx -row 3 -column 3
	grid $t.ph1.entryy -row 3 -column 4
	grid $t.ph1.entryz -row 3 -column 5
	grid $t.ph1.op -row 1 -column 6
	grid $t.ph1.ad -row 2 -column 6
	grid $t.ph1.dl -row 3 -column 6
	# grid $t.ph1.ck -row 3 -column 6

	pack $t.ph1
	#table of the pharmacophore cluster
	# set p [frame $t.ph1.subtable]
	frame $t.subtable
	ttk::treeview $t.subtable.tree -yscroll "$t.subtable.sb set"
	scrollbar $t.subtable.sb -command "$t.subtable.tree yview" -orient vertical

	grid $t.subtable.tree $t.subtable.sb -sticky nsew
	grid column $t.subtable 0 -weight 1
	grid row $t.subtable 5 -weight 1
	pack $t.subtable -fill x

	# $t.subtable.tree insert {} end -text "TEST"

	#pharmocheore number 2
	frame $t.ph2
	label $t.ph2.label01 -text "\nThe SECOND pharmacophore cluster."
	label $t.ph2.label02 -text "Variable name"
	label $t.ph2.label03 -text "Pharmacophore type"
	label $t.ph2.labelx -width 8 -text "X"
	label $t.ph2.labely -width 8 -text "Y"
	label $t.ph2.labelz -width 8 -text "Z"
	entry $t.ph2.entry1 -width 12 -textvariable ::elixir::ph2vn 
	entry $t.ph2.entryx -textvariable ::elixir::ph2x -width 8
	entry $t.ph2.entryy -textvariable ::elixir::ph2y -width 8
	entry $t.ph2.entryz -textvariable ::elixir::ph2z -width 8
	button $t.ph2.op -text "Import from pdb" -command ::elixir::openprotein2
	button $t.ph2.ad -text Add -command ::elixir::ph2add -width 5
	button $t.ph2.ck -text Check -command ::elixir::checkstatus2
	button $t.ph2.dl -text Delete -command ::elixir::ph2del

	#geometry box
	grid $t.ph2.label01 -row 1 -columnspan 5
	grid $t.ph2.label02 -row 2 -column 1
	grid $t.ph2.entry1  -row 2 -column 2
	grid $t.ph2.labelx -row 2 -column 3
	grid $t.ph2.labely -row 2 -column 4
	grid $t.ph2.labelz -row 2 -column 5
	grid $t.ph2.label03 -row 3 -column 1
	grid [ttk::combobox $t.ph2.listbox1 -width 18 -textvariable ::elixir::ph2type \
	 	-values [list Default Hydrophobic Aromatic HydrogenDonor HydeogenAcceptor Positivelon Negativelon ExclusionSphere] -state readonly] \
	 	-row 3 -column 2
	grid $t.ph2.entryx -row 3 -column 3
	grid $t.ph2.entryy -row 3 -column 4
	grid $t.ph2.entryz -row 3 -column 5
	grid $t.ph2.op -row 1 -column 6
	grid $t.ph2.ad -row 2 -column 6
	grid $t.ph2.dl -row 3 -column 6
	# grid $t.ph2.ck -row 3 -column 6

	pack $t.ph2
	#table of the pharmacophore cluster
	# set p [frame $t.ph1.subtable]
	frame $t.subtable2
	ttk::treeview $t.subtable2.tree -yscroll "$t.subtable2.sb set"
	scrollbar $t.subtable2.sb -command "$t.subtable2.tree yview" -orient vertical

	grid $t.subtable2.tree $t.subtable2.sb -sticky nsew
	grid column $t.subtable2 0 -weight 1
	grid row $t.subtable2 5 -weight 1
	pack $t.subtable2 -fill x

	# $t.subtable2.tree insert {} end -text "TEST2"

	#The output frame
	frame $t.op
	label $t.op.label00 -text "\nOutput Configurations"
	label $t.op.label01 -text "Output directory"
	entry $t.op.cd -textvariable ::elixir::outputfolder -width 50
	# entry $t.op.cd -textvariable ::elixir::outputfolder -width 50 -state disable
	button $t.op.browse -width 6 -text "Browse" -command {
		set tmp [tk_chooseDirectory]
		if {![string equal $tmp ""]} {
			set ::elixir::outputfolder $tmp
		}
	}
	grid $t.op.label00 -pady 10
	grid $t.op.label01 $t.op.cd $t.op.browse -pady 0
	pack $t.op
	frame $t.op2
	label $t.op2.label02 -text "Output file type(s) (optional):    "
	#1.log output 2.json output 
	label $t.op2.cbl01 -text ".log    "
	label $t.op2.cbl02 -text ".json"
	checkbutton $t.op2.cb1 -state normal -variable ::elixir::logout
	checkbutton $t.op2.cb2 -state normal -variable ::elixir::jsonout
	label $t.op2.cb03 -text "Number of iterations: "
	entry $t.op2.cb3 -width 8 -textvariable ::elixir::numiterations -state disable
	label $t.op2.cb04 -text "Maximum threshold: "
	entry $t.op2.cb4 -width 8 -textvariable ::elixir::threshold -state disable

	grid $t.op2.label02 $t.op2.cb1 $t.op2.cbl01 $t.op2.cb2 $t.op2.cbl02 
	grid $t.op2.cb03 $t.op2.cb3 $t.op2.cb04 $t.op2.cb4 
	pack $t.op2 -fill x
	# grid $t.op.cb1 $t.op.cbl01 $t.op.cb2 $t.op.cbl02 -sticky nsew
	
	#set some buttons for the function
	frame $t.bot
	button $t.bot.s -text Sumbit -command ::elixir::call_python
	pack $t.bot.s -side top -pady 10 -fill x
	pack $t.bot -side top -pady 2 -fill x

	return $t
}

proc ::elixir::openprotein {} \
{
	variable t;
	variable ph1prt;
	variable ph1id "";
	set ph1prt [tk_getOpenFile -filetypes {{pdb {.pdb}} {all {.*}}} ]
	set ph1id [mol new $ph1prt]
	mol modstyle 0 $ph1id vDw 0.4
	mol modcolor 0 $ph1id colorID 7
	#show the first cluster in red vdw format.


	for {set i 0} {$i < [[atomselect $ph1id all] num]} {incr i} {
		set ::elixir::ph1vn [lindex [[atomselect $ph1id all] get resname] $i]
		set ::elixir::ph1type "Default"
		set ::elixir::ph1x [lindex [[atomselect $ph1id all] get x] $i]
		set ::elixir::ph1y [lindex [[atomselect $ph1id all] get y] $i]
		set ::elixir::ph1z [lindex [[atomselect $ph1id all] get z] $i]
		::elixir::ph1add
	}
	
}


proc ::elixir::ph1add {} {
	variable t;
	append ::elixir::ph1data " " [list "$::elixir::ph1vn,$::elixir::ph1type,$::elixir::ph1x,$::elixir::ph1y,$::elixir::ph1z"]
	# $t.subtable.tree insert {} end -id $::elixir::ph1index -text [lindex $::elixir::ph1data $::elixir::ph1index]
	$t.subtable.tree insert {} end -id $::elixir::ph1index -text "$::elixir::ph1vn   $::elixir::ph1x: $::elixir::ph1y: $::elixir::ph1z $::elixir::ph1type"
	$t.subtable.tree insert $::elixir::ph1index end -id [expr {$::elixir::ph1index + 0.1}] -text "Pharmacophore type:  $::elixir::ph1type"
	$t.subtable.tree insert $::elixir::ph1index end -id [expr {$::elixir::ph1index + 0.2}] -text "X:  $::elixir::ph1x"
	$t.subtable.tree insert $::elixir::ph1index end -id [expr {$::elixir::ph1index + 0.3}] -text "Y:  $::elixir::ph1y"
	$t.subtable.tree insert $::elixir::ph1index end -id [expr {$::elixir::ph1index + 0.4}] -text "Z:  $::elixir::ph1z"
	# puts [lindex $::elixir::ph1data $::elixir::ph1index]
	# puts $::elixir::ph1data

	lset ::elixir::ph1indexs 0 $::elixir::ph1index 1
	set ::elixir::ph1index [expr {$::elixir::ph1index + 1}]
}

proc ::elixir::ph1del {} {
	variable t;
	if {![string equal [$t.subtable.tree selection] ""]} {
		lset ::elixir::ph1indexs 0 [::tcl::mathfunc::round [$t.subtable.tree selection]] 0
		$t.subtable.tree delete [::tcl::mathfunc::round [$t.subtable.tree selection]]
		#Check the status of the selected atom	
	}
}

proc ::elixir::checkstatus {} {
	variable t;
	puts [::tcl::mathfunc::round [$t.subtable.tree selection]]
	# puts [$t.subtable.tree selection]
}

proc ::elixir::ph2add {} {
	variable t;
	append ::elixir::ph2data " " [list "$::elixir::ph2vn,$::elixir::ph2type,$::elixir::ph2x,$::elixir::ph2y,$::elixir::ph2z"]
	# $t.subtable2.tree insert {} end -id $::elixir::ph2index -text [lindex $::elixir::ph2data $::elixir::ph2index]
	$t.subtable2.tree insert {} end -id $::elixir::ph2index -text "$::elixir::ph2vn   $::elixir::ph2x: $::elixir::ph2y: $::elixir::ph2z $::elixir::ph2type"
	$t.subtable2.tree insert $::elixir::ph2index end -id [expr {$::elixir::ph2index + 0.1}] -text "Pharmacophore type:  $::elixir::ph2type"
	$t.subtable2.tree insert $::elixir::ph2index end -id [expr {$::elixir::ph2index + 0.2}] -text "X:  $::elixir::ph2x"
	$t.subtable2.tree insert $::elixir::ph2index end -id [expr {$::elixir::ph2index + 0.3}] -text "Y:  $::elixir::ph2y"
	$t.subtable2.tree insert $::elixir::ph2index end -id [expr {$::elixir::ph2index + 0.4}] -text "Z:  $::elixir::ph2z"
	# puts [lindex $::elixir::ph2data $::elixir::ph2index]
	# puts $::elixir::ph2data
	lset ::elixir::ph2indexs 0 $::elixir::ph2index 1
	set ::elixir::ph2index [expr {$::elixir::ph2index + 1}]
}

proc ::elixir::ph2del {} {
	variable t;
	if {![string equal [$t.subtable2.tree selection] ""]} {
		lset ::elixir::ph2indexs 0 [::tcl::mathfunc::round [$t.subtable2.tree selection]] 0
		$t.subtable2.tree delete [::tcl::mathfunc::round [$t.subtable2.tree selection]]
		# lset ::elixir::ph2indexs 0 [$t.subtable2.tree selection] 0
		#Check the status of the selected atom
	}

}

proc ::elixir::checkstatus2 {} {
	variable t;
	puts $t.subtable2.tree [$t.subtable2.tree selection]
}

proc ::elixir::openprotein2 {} \
{
	variable t;
	variable ph2prt;
	variable ph2id "";
	set ph2prt [tk_getOpenFile -filetypes {{pdb {.pdb}} {all {.*}}} ]
	set ph2id [mol new $ph2prt]
	mol modstyle 0 $ph2id vDw 0.4
	mol modcolor 0 $ph2id colorID 1
	#show the second cluster in red vdw format.

	for {set i 0} {$i < [[atomselect $ph2id all] num]} {incr i} {
		set ::elixir::ph2vn [lindex [[atomselect $ph2id all] get resname] $i]
		set ::elixir::ph2type "Default"
		set ::elixir::ph2x [lindex [[atomselect $ph2id all] get x] $i]
		set ::elixir::ph2y [lindex [[atomselect $ph2id all] get y] $i]
		set ::elixir::ph2z [lindex [[atomselect $ph2id all] get z] $i]
		::elixir::ph2add
	}
	
}

proc ::elixir::call_python {} {

# set output [exec python [file join $::env(ELIXIRDIR) "elixirA.py"]] [list $::elixir::ph2indexs]
# set output [exec python "hello.py" [list [expr {$::elixir::ph1index -1}] $::elixir::ph1indexs [expr {$::elixir::ph2index -1}] $::elixir::ph2indexs] \
#  [list $::elixir::ph1data $::elixir::ph2data]]

set output [exec python [file join $::env(ELIXIRDIR) "elixirA.py"] [expr {$::elixir::ph1index -1}] $::elixir::ph1indexs [expr {$::elixir::ph2index -1}] $::elixir::ph2indexs \
 $::elixir::ph1data $::elixir::ph2data $::elixir::outputfolder]
#test on 
# set output [exec python [file join $::env(ELIXIRDIR) "elixirA.py"] [list $::elixir::molsx11 $::elixir::molsy11 $::elixir::molsz11 \
# 	$::elixir::molsx12 $::elixir::molsy12 $::elixir::molsz12 \
# 	$::elixir::molsx13 $::elixir::molsy13 $::elixir::molsz13 \
# 	$::elixir::molsx14 $::elixir::molsy14 $::elixir::molsz14 \
# 	$::elixir::molsx15 $::elixir::molsy15 $::elixir::molsz15 \
# 	$::elixir::molsx21 $::elixir::molsy21 $::elixir::molsz21 \
# 	$::elixir::molsx22 $::elixir::molsy22 $::elixir::molsz22 \
# 	$::elixir::molsx23 $::elixir::molsy23 $::elixir::molsz23 \
# 	$::elixir::molsx24 $::elixir::molsy24 $::elixir::molsz24 \
# 	$::elixir::molsx25 $::elixir::molsy25 $::elixir::molsz25 \
# 	]]
puts $output

if {[string equal $::elixir::outputfolder ""]} {
	set outputpdb [mol new output.pdb]
	mol modstyle 0 $outputpdb vDw 0.4
	mol modcolor 0 $outputpdb colorID 4
} else {
	set pdbdir $::elixir::outputfolder/output.pdb
	set outputpdb [mol new $pdbdir]
	mol modstyle 0 $outputpdb vDw 0.4
	mol modcolor 0 $outputpdb colorID 4
}

}

proc elixir_tk {} {
	::elixir::elixirgui
	
}
