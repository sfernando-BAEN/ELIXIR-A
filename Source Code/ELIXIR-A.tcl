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
## 0.9 Update on the JSON output.
## 1.0 Fix bugs.
## 2.0 Use open3d as the source of icp algorithm.
## 2.1 Receptor protein can be loaded via the GUI.

package provide elixir 2.1
package require tile
variable ELIXIRDIR

namespace eval ::elixir:: {
	# namespace export Elixir
	variable w;
	variable t;
	variable v;
	variable inputfolder_1 "ELIXIR-A_01.pdb"
	variable inputfolder_2 "ELIXIR-A_02.pdb"
	variable inputfolder_3 ""
	variable pyt "python"
	variable g_voxel "0.5"
	variable iter "100"
	variable rfit "0.1"
	variable rrmse "0.1"
	variable suffix1 "_source_out.pdb"
	variable suffix2 "_target_out.pdb"
	variable dthreshold "2"
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
	#wm resizable $t 1 1
	#wm geometry $t 300x460+150+50
	wm title $t "Enhanced Ligand Exploration and Interaction Recognition Algorithm"

	#The first input frame
	frame $t.ip1
	label $t.ip1.label00 -text "\nThe first pharmacophore cluster (source point cloud)"
	label $t.ip1.label01 -text "Input pdb file:"
	entry $t.ip1.cd -textvariable ::elixir::inputfolder_1 -width 50

	button $t.ip1.browse -width 6 -text "Browse" -command {
		set tmp [tk_getOpenFile]
		if {![string equal $tmp ""]} {
			set ::elixir::inputfolder_1 $tmp
		}
	}
	grid $t.ip1.label00     -row 1 -column 1 -columnspan 3 -sticky w 
	grid $t.ip1.label01     -row 2 -column 1 -columnspan 1 -sticky w 
	grid $t.ip1.cd          -row 2 -column 2 -columnspan 1 -sticky w 
	grid $t.ip1.browse      -row 2 -column 3 -columnspan 1 -sticky w
    #pack $t.ip1

	#The second input frame
	frame $t.ip2
	label $t.ip2.label00 -text "\nThe second pharmacophore cluster (target point cloud)"
	label $t.ip2.label01 -text "Input pdb file:"
	entry $t.ip2.cd -textvariable ::elixir::inputfolder_2 -width 50

	button $t.ip2.browse -width 6 -text "Browse" -command {
		set tmp [tk_getOpenFile]
		if {![string equal $tmp ""]} {
			set ::elixir::inputfolder_2 $tmp
		}
	}

	#geometry box
	grid $t.ip2.label00     -row 1 -column 1 -columnspan 3 -sticky w 
	grid $t.ip2.label01     -row 2 -column 1 -columnspan 1 -sticky w 
	grid $t.ip2.cd          -row 2 -column 2 -columnspan 1 -sticky w 
	grid $t.ip2.browse      -row 2 -column 3 -columnspan 1 -sticky w
    #pack $t.ip2

    #Recepotor
	frame $t.re2
	label $t.re2.label00 -text "\nTarget receptor. Please load the receptor after submission of pharmacopeial refinement. (Optional)"
	label $t.re2.label01 -text "Input pdb file:"
	entry $t.re2.cd -textvariable ::elixir::inputfolder_3 -width 39

	button $t.re2.browse -width 6 -text "Browse" -command {
		set tmp [tk_getOpenFile]
		if {![string equal $tmp ""]} {
			set ::elixir::inputfolder_3 $tmp
		}
	}

	button $t.re2.load -width 6 -text "Load" -command {
		if {![string equal $::elixir::inputfolder_3 ""]} {
			set pdbdir $::elixir::inputfolder_3
			set outputpdb3 [mol new $pdbdir]
			#mol addrep $outputpdb1
			mol modstyle 0 $outputpdb3 NewCartoon
			mol modcolor 0 $outputpdb3 colorID 10
			mol modselect 0 $outputpdb3 "protein"

			mol addrep $outputpdb3
			mol modstyle 1 $outputpdb3 Bonds
			mol modcolor 1 $outputpdb3 Name
			mol modselect 1 $outputpdb3 "not protein and not water"
		}
	}
	#geometry box
	grid $t.re2.label00     -row 1 -column 1 -columnspan 4 -sticky w 
	grid $t.re2.label01     -row 2 -column 1 -columnspan 1 -sticky w 
	grid $t.re2.cd          -row 2 -column 2 -columnspan 1 -sticky w 
	grid $t.re2.browse      -row 2 -column 3 -columnspan 1 -sticky w
    grid $t.re2.load        -row 2 -column 4 -columnspan 1 -sticky w

	#Parameter
	labelframe $t.pm -text "Input parameter" -padx 2 -pady 4
	label $t.pm.g_label_1 -text "Global registration with RANSAC iteration"
	
	entry $t.pm.gvoxel -width 5 -textvariable ::elixir::g_voxel
	label $t.pm.gvoxel_l -text "Voxel size:"

	label $t.pm.cicp_1 -text "Colored point cloud registration"
	entry $t.pm.iters -width 5 -textvariable ::elixir::iter
	label $t.pm.iters_1 -text "Maximum iterations:"
	entry $t.pm.r_fit -width 5 -textvariable ::elixir::rfit
	label $t.pm.r_fit_1 -text "Relative_fitness:"
	entry $t.pm.r_rmse -width 5 -textvariable ::elixir::rrmse
	label $t.pm.r_rmse_1 -text "Relative_RMSE (Å):"	
	entry $t.pm.dthre -width 5 -textvariable ::elixir::dthreshold
	label $t.pm.dthre_1 -text "Correspondence distance threshold (Å):"	

	grid $t.pm.g_label_1 -row 1 -column 1 -columnspan 1 -sticky w
	grid $t.pm.gvoxel_l -row 2 -column 1 -columnspan 1 -sticky w
	grid $t.pm.gvoxel -row 2 -column 2 -columnspan 1 -sticky w
	grid $t.pm.cicp_1 -row 3 -column 1 -columnspan 1 -sticky w
	grid $t.pm.iters_1 -row 4 -column 1 -columnspan 1 -sticky w
	grid $t.pm.iters -row 4 -column 2 -columnspan 1 -sticky w
	grid $t.pm.r_fit_1 -row 5 -column 1 -columnspan 1 -sticky w
	grid $t.pm.r_fit -row 5 -column 2 -columnspan 1 -sticky w
	grid $t.pm.r_rmse_1 -row 6 -column 1 -columnspan 1 -sticky w
	grid $t.pm.r_rmse -row 6 -column 2 -columnspan 1 -sticky w
	grid $t.pm.dthre_1 -row 7 -column 1 -columnspan 1 -sticky w
	grid $t.pm.dthre -row 7 -column 2 -columnspan 1 -sticky w

	#Options
	frame $t.op
	label $t.op.pyt_1 -text "Python3 launcher command:"
	entry $t.op.pyt_c -width 10 -textvariable ::elixir::pyt


	grid $t.op.pyt_1 -row 1 -column 1 -columnspan 1 -sticky w
	grid $t.op.pyt_c -row 1 -column 2 -columnspan 1 -sticky w

	#set some buttons for the function
	frame $t.bot
	button $t.bot.s -text "Submit" -width 70 -command ::elixir::call_python
	grid $t.bot.s -row 1 -column 1 -columnspan 1 -sticky we


	grid $t.ip1 -row 1 -column 1 -columnspan 3 -sticky we -padx 2 -pady 3
	grid $t.ip2 -row 2 -column 1 -columnspan 3 -sticky we -padx 2 -pady 3
	grid $t.re2 -row 3 -column 1 -columnspan 4 -sticky we -padx 2 -pady 3
	grid $t.pm -row 4 -column 1 -columnspan 3 -sticky we -padx 6 -pady 3
	grid $t.op -row 5 -column 1 -columnspan 3 -sticky we -padx 2 -pady 3
	grid $t.bot -row 6 -column 1 -columnspan 1 -sticky we -padx 6 -pady 3

	return $t


}

proc ::elixir::call_python {} {

set output [exec $::elixir::pyt [file join $::env(ELIXIRDIR) "ELIXIR-A_open3d.py"] $::elixir::inputfolder_1 $::elixir::inputfolder_2 \
$::elixir::g_voxel $::elixir::iter $::elixir::rfit $::elixir::rrmse $::elixir::dthreshold]



foreach i [molinfo list] { mol delete $i }
color Display Background white

set pdbdir $::elixir::inputfolder_1$::elixir::suffix1
set outputpdb1 [mol new $pdbdir]
#mol addrep $outputpdb1
mol modstyle 0 $outputpdb1 vDw 0.3
mol modcolor 0 $outputpdb1 colorID 3
mol modselect 0 $outputpdb1 "resname is HAC"

mol addrep $outputpdb1
mol modstyle 1 $outputpdb1 vDw 0.3
mol modcolor 1 $outputpdb1 colorID 6
mol modselect 1 $outputpdb1 "resname is HDR"

mol addrep $outputpdb1
mol modstyle 2 $outputpdb1 vDw 0.6
mol modcolor 2 $outputpdb1 colorID 7
mol modselect 2 $outputpdb1 "resname is HPB"

mol addrep $outputpdb1
mol modstyle 3 $outputpdb1 vDw 0.66
mol modcolor 3 $outputpdb1 colorID 11
mol modselect 3 $outputpdb1 "resname is ARO"

mol addrep $outputpdb1
mol modstyle 4 $outputpdb1 vDw 0.45
mol modcolor 4 $outputpdb1 colorID 1
mol modselect 4 $outputpdb1 "resname is NIO"

mol addrep $outputpdb1
mol modstyle 5 $outputpdb1 vDw 0.45
mol modcolor 5 $outputpdb1 colorID 0
mol modselect 5 $outputpdb1 "resname is PIO"


set pdbdir $::elixir::inputfolder_2$::elixir::suffix2
set outputpdb2 [mol new $pdbdir]
#mol addrep $outputpdb2
mol modstyle 0 $outputpdb2 vDw 0.5
mol modcolor 0 $outputpdb2 colorID 3
mol modselect 0 $outputpdb2 "resname is HAC"
mol modmaterial 0 $outputpdb2 Transparent

mol addrep $outputpdb2
mol modstyle 1 $outputpdb2 vDw 0.5
mol modcolor 1 $outputpdb2 colorID 6
mol modselect 1 $outputpdb2 "resname is HDR"
mol modmaterial 1 $outputpdb2 Transparent

mol addrep $outputpdb2
mol modstyle 2 $outputpdb2 vDw 1.0
mol modcolor 2 $outputpdb2 colorID 7
mol modselect 2 $outputpdb2 "resname is HPB"
mol modmaterial 2 $outputpdb2 Transparent

mol addrep $outputpdb2
mol modstyle 3 $outputpdb2 vDw 1.1
mol modcolor 3 $outputpdb2 colorID 11
mol modselect 3 $outputpdb2 "resname is ARO"
mol modmaterial 3 $outputpdb2 Transparent

mol addrep $outputpdb2
mol modstyle 4 $outputpdb2 vDw 0.75
mol modcolor 4 $outputpdb2 colorID 1
mol modselect 4 $outputpdb2 "resname is NIO"
mol modmaterial 4 $outputpdb2 Transparent

mol addrep $outputpdb2
mol modstyle 5 $outputpdb2 vDw 0.75
mol modcolor 5 $outputpdb2 colorID 0
mol modselect 5 $outputpdb2 "resname is PIO"
mol modmaterial 5 $outputpdb2 Transparent

puts $output
}


proc elixir_tk {} {
	::elixir::elixirgui
	
}








