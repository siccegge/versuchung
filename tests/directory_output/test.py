from __future__ import print_function

from versuchung.experiment import Experiment
from versuchung.types import String
from versuchung.files import Directory
import os

class SimpleExperiment(Experiment):
    outputs = {"dir1": Directory("d1"),
               "dir2": Directory("d2")}

    def run(self):
        a = self.o.dir1.new_file("barfoo")
        a.value="abc"
        a.flush()
        os.mkdir(self.o.dir1.path + "/tmpdir")
        with open(self.o.dir1.path + "/tmpdir/foo", "w+") as fd:
            fd.write("Hallo")

        self.o.dir2.mirror_directory(self.o.dir1.path,
                                     lambda x: True)

if __name__ == "__main__":
    import shutil, sys,os
    experiment = SimpleExperiment()
    dirname = experiment(sys.argv)

    assert os.path.isdir(experiment.o.dir2.path + "/tmpdir")
    assert os.path.exists(experiment.o.dir2.path + "/barfoo")
    assert os.path.exists(experiment.o.dir2.path + "/tmpdir/foo")

    if dirname:
        shutil.rmtree(dirname)
    print("success")
