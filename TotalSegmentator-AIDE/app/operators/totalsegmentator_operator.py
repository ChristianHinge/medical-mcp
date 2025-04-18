# TotalSegmentator operator
#
# This operator uses TotalSegmentator (https://github.com/wasserth/TotalSegmentator) to perform automated segmentation
# of 104 regions in CT imaging data. TotalSegmentator is created by University Hospital Basel.
#

import logging
import os
import subprocess
import shutil
import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, InputContext, IOType, Operator, OutputContext, OperatorSpec


# @md.input("nii_ct_dataset", DataPath, IOType.DISK)
# @md.output("nii_seg_output_path", DataPath, IOType.DISK)
# @md.env(pip_packages=["pydicom >= 2.3.0", "highdicom >= 0.18.2"])
class TotalSegmentatorOperator(Operator):
    """
    TotalSegmentator Operator - perform segmentation on CT imaging data saved as NIFTI file
    """
    def __init__(self, fragment):
        super().__init__(fragment)

    def setup(self,spec):
        spec.input("nii_ct_dataset")
        spec.output("nii_seg_output_path")

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        logging.info(f"Begin {self.compute.__name__}")

        # collect ct_nifti_dataset
        nii_input_file = op_input.receive("nii_ct_dataset").path

        if not os.path.exists(nii_input_file):
            NameError('Exception occurred with nii_input_file')
        else:
            logging.info(f"Found nii_input_file: {nii_input_file}")

        # Create TotalSegmentator output directory
        nii_seg_output_path = "nii_seg_output"
        if not os.path.exists(nii_seg_output_path):
            os.makedirs(nii_seg_output_path)

        # Run TotalSegmentator
        subprocess.run(["TotalSegmentator", "-i", nii_input_file, "-o", nii_seg_output_path])

        # Local testing - copy from local_files directory e.g. local_files in repo root (hardcode this yourself)
        # src = '../../local_files/nii_seg_output'
        # for file in os.listdir(src):
        #    shutil.copy2(os.path.join(src, file), nii_seg_output_path)

        logging.info("Performed TotalSegmentator processing")

        # Set output path for next operator
        op_output.emit(DataPath(os.path.abspath(nii_seg_output_path)), "nii_seg_output_path")
        logging.info(f"End {self.compute.__name__}")
