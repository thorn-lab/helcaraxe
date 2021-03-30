import os, sys
import glob
from subprocess import Popen, PIPE, STDOUT


def addSym2Cif(l_symm, l_cell, t_code, t_cif, t_pdb):
    print("addSym2Cif {}, {}, {}, {}, {}".format(l_symm, l_cell, t_code, t_cif, t_pdb))

    try:
        aCif = open(t_cif, "r+")
    except IOError:
        print("%s could not be found for reading" % t_cif)
        return False
    else:
        title = ""
        t_begin = True
        i = 0
        while i < 4 and t_begin:
            a_l = aCif.readline()
            if a_l.strip()[:6].find("data_r") != -1:
                t_begin = False
            title += a_l
            i = i + 1

        rest = aCif.readlines()

        # if part of all cell and symm info missing

        if not l_symm or not l_cell:
            # get them from PDB
            try:
                aPdb = open(t_pdb, "r")
            except IOError:
                print("%s could not be found for reading" % t_pdb)
                return False
            else:
                # cell paras
                length_a = ""
                length_b = ""
                length_c = ""
                angle_alpha = ""
                angle_beta = ""
                angle_gamma = ""
                formula_units_Z = ""

                # space group
                space_group_name_H_M = ""
                entry_id = t_code

                for aLine in aPdb.readlines():
                    aLstrs = aLine.strip().split()[0]
                    if aLstrs.find("CRYST1") != -1:
                        length_a = aLine[6:15]
                        length_b = aLine[15:24]
                        length_c = aLine[24:33]
                        angle_alpha = aLine[33:40]
                        angle_beta = aLine[40:47]
                        angle_gamma = aLine[47:54]

                        space_group_name_H_M = aLine[55:66]

                        formula_units_Z = aLine[66:].strip()

                        break

                aPdb.close()

                aCif.seek(0)
                aCif.write(title)

                # add the symm and cell info from the secondline of the file
                if not l_cell:
                    aCif.write("\n")
                    aCif.write("_cell.entry_id %s \n" % entry_id.center(20))
                    aCif.write("_cell.length_a %s \n" % length_a.center(20))
                    aCif.write("_cell.length_b %s \n" % length_b.center(20))
                    aCif.write("_cell.length_c %s \n" % length_c.center(20))
                    aCif.write("_cell.angle_alpha %s \n" % angle_alpha.center(20))
                    aCif.write("_cell.angle_beta %s \n" % angle_beta.center(20))
                    aCif.write("_cell.angle_gamma %s \n" % angle_gamma.center(20))
                    aCif.write("_cell.formula_units_Z %s \n" % formula_units_Z.center(10))

                if not l_symm:
                    aCif.write("\n")
                    aCif.write("_symmetry.entry_id %s \n" % entry_id.center(20))
                    t_str = "'%s'" % space_group_name_H_M.strip()
                    aCif.write("_symmetry.space_group_name_H-M %s\n" % t_str.center(20))
                    aCif.write("\n")

                for aLine in rest:
                    aCif.write(aLine)

        aCif.close()

        return True


class MTZGENERATOR:

    def __init__(self):

        self.mmcif_kw = []

        self.get_mmcif_kw()

        self.dir_in = ""
        self.dir_out = ""

        self.dir_bad = ""
        self.dir_scr = ""

        # self.cif2mtz = os.path.join(os.getenv("CBIN"), "cif2mtz")
        self.cif2mtz = "/Applications/ccp4-7.1/bin/cif2mtz"

        # self.sh = os.getenv("SHELL").strip().split("/")[-1]
        # print self.sh
        # aCMD = "source /lmb/home/flong/CCP4/ccp4-7.0/bin/ccp4.setup-sh"
        # if self.sh.find("csh") != -1:
        #    aCMD = "source /lmb/home/flong/CCP4/ccp4-7.0/bin/ccp4.setup-csh"
        # os.system(aCMD)
        # print os.getenv("CCP4")

    def get_mmcif_kw(self):

        cif_dict_name = os.path.join("/Applications/ccp4-7.1/share/ccif", "cif_mm.dic")
        try:
            cif_dict = open(cif_dict_name, "r")
        except IOError:
            print("ccp4 cif dictionary file can not be opened for reading")
            sys.exit()
        else:
            for a_line in cif_dict.readlines():
                strgrp = a_line.strip().split()
                if len(strgrp) == 1:
                    if strgrp[0].find("save_") != -1 and len(strgrp[0]) > 5:
                        self.mmcif_kw.append(strgrp[0].strip()[5:].upper())

            self.mmcif_kw.append("_audit.revision_id")
            cif_dict.close()

    def filterCif(self, t_fin, t_fout):
        print("filterCif {}, {}".format(t_fin, t_fout))
        if os.path.isfile(t_fin):
            try:
                cif_in_obj = open(t_fin, "r")
            except IOError:
                print("%s can not be opened for reading" % t_fin)
                sys.exit()
            else:
                cif_out_obj = open(t_fout, "w")

                n_l = 0
                entry_absent = []
                for a_line in cif_in_obj.readlines():
                    if len(a_line) > 0:
                        if a_line.find("loop_") != -1:
                            n_l = 0
                            entry_absent = []
                        strgrp1 = a_line.strip().split()
                        line_len = len(strgrp1)
                        if line_len == 1 and a_line[0].find("_") != -1 and a_line.find("_symmetry_equiv") == -1:
                            if strgrp1[0].strip().upper() in self.mmcif_kw:
                                cif_out_obj.write(a_line)
                            else:
                                entry_absent.append(n_l)
                            n_l += 1
                        elif (a_line[0].find("_") != -1) and line_len >= 2:
                            cif_out_obj.write(a_line)
                        elif a_line[0].find("#") == -1:
                            if line_len == n_l:
                                str_spa = "    "
                                a_pline = ""
                                for i in range(line_len):
                                    if not i in entry_absent:
                                        a_pline += (strgrp1[i] + str_spa)
                                cif_out_obj.write(a_pline + "\n")
                            else:
                                cif_out_obj.write(a_line)
                        else:
                            cif_out_obj.write(a_line)

                    if (a_line.find("#CRYST1") != -1 or a_line.find("_cell.length_a") != -1) and not self.has_cell:
                        self.has_cell = True

                    if (a_line.find("#CRYST1") != -1 or a_line.find("_symmetry.entry_id") != -1) and not self.has_symm:
                        self.has_symm = True

                cif_out_obj.close()

                cif_in_obj.close()

    def execute(self, t_dirs):

        self.dir_cif_in = t_dirs[0]
        self.dir_pdb_in = t_dirs[1]
        self.dir_out = t_dirs[2]

        if not glob.glob(self.dir_out):
            os.makedirs(self.dir_out, exist_ok=True)

        self.dir_bad = os.path.join(self.dir_out, "bad_files")
        if not glob.glob(self.dir_bad):
            os.makedirs(self.dir_bad, exist_ok=True)

        self.dir_scr = os.path.join(self.dir_out, "scr_files")
        if not glob.glob(self.dir_scr):
            os.makedirs(self.dir_scr, exist_ok=True)

        for cifName in glob.glob(self.dir_cif_in + "/*-sf.cif"):
            self.has_cell = False
            self.has_symm = False

            pdbCode = os.path.basename(cifName).strip().split(".")[0][0:4]
            print('========{0}======'.format(pdbCode))
            pdbName = os.path.join(self.dir_pdb_in, pdbCode + ".pdb")

            newCifName = os.path.join(self.dir_scr, pdbCode + ".cif")
            aMtzName = os.path.join(self.dir_out, pdbCode + "-sf.mtz")
            if (not glob.glob(aMtzName)):
                print(cifName)
                print(pdbName)
                self.filterCif(cifName, newCifName)

                lPass = True
                if not self.has_cell or not self.has_symm:
                    lPass = False
                    # print "The orignal cif file %s does not contain either symmetry or cell or both infortion"%cifName
                    # print "Those data are read from the correspond pdb files and added into a new cif file "
                    lPass = addSym2Cif(self.has_symm, self.has_cell, pdbCode, newCifName, pdbName)
                if lPass:
                    aMtzName = os.path.join(self.dir_out, pdbCode + "-sf.mtz")
                    # aMtzLog  = os.path.join(self.dir_scr, "cif2mtz_"+pdbCode + ".log")
                    # cmdline = "%s hklin %s hklout %s > %s \n"%(self.cif2mtz, newCifName, aMtzName, aMtzLog)
                    # cmdline = 'echo \"end\" | ' + cmdline
                    # cmdline += "end\n"
                    # cmdline += "eof\n"

                    args = [self.cif2mtz, 'hklin', newCifName, 'hklout', aMtzName]
                    print(' >> ' + ' '.join(args))
                    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    outputTuple = p.communicate(b'end\n')
                    if p.returncode != 0:
                        print(aMtzName + ": " + str(outputTuple))
                        #raise MtzGenError(p.returncode)

    def execute2(self, tPdbName, tCifName, tMtzName, tCode, tScrDir, tLog):
        self.has_cell = False
        self.has_symm = False

        newCifName = os.path.join(tScrDir, tCode + ".cif")
        self.filterCif(tCifName, newCifName)

        lPass = True
        if not self.has_cell or not self.has_symm:
            lPass = False
            print("The orignal cif file %s does not contain either symmetry or cell or both infortion" % tCifName)
            print("Those data are read from the correspond pdb files and added into a new cif file ")
            lPass = addSym2Cif(self.has_symm, self.has_cell, tCode, newCifName, tPdbName)

        if lPass:
            args = [self.cif2mtz, 'hklin', newCifName, 'hklout', tMtzName]
            print(' >> ' + ' '.join(args))
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            outputTuple = p.communicate(b'end\n')
            if p.returncode != 0:
                print(tMtzName + ": " + str(outputTuple))
                #raise MtzGenError(p.returncode)
            return p.returncode
        else:
            print("Failed to add the symmetrical info to %s  " % newCifName)

mtz = MTZGENERATOR()
mtz.execute(t_dirs=["/Users/kristophernolte/Documents/test_mmCIF", "/Users/kristophernolte/Documents/test_pdb", "/Users/kristophernolte/Documents/test_mtz"])