# TotalSegmentator AIDE App
#
# TotalSegmentator is a tool for robust segmentation of 104 important anatomical structures in CT images.
# Website: https://github.com/wasserth/TotalSegmentator
#
# TotalSegmentator is distributed under the Apache 2.0 licence. The code in this MONAI Application Package (MAP) is not
# created by the original developers of TotalSegmentator. TotalSegmentator is created by University Hospital Basel.
#
# Tom Roberts (tom.roberts@gstt.nhs.uk / t.roberts@kcl.ac.uk)
# Anil Mistry (anil.mistry@gstt.nhs.uk / anil.mistry@kcl.ac.uk)
#

import logging

from monai.deploy.core import Application
from monai.deploy.operators.dicom_utils import ModelInfo
from monai.deploy.operators import DICOMEncapsulatedPDFWriterOperator
from monai.deploy.operators import DICOMSeriesSelectorOperator
from monai.deploy.operators import DICOMDataLoaderOperator, DICOMSeriesToVolumeOperator
from operators.dcm2nii_operator import Dcm2NiiOperator
from operators.rtstructwriter_operator import RTStructWriterOperator
from operators.totalsegmentator_operator import TotalSegmentatorOperator
from operators.clinrev_pdf_operator import ClinicalReviewPDFGenerator



class TotalSegmentatorApp(Application):
    """
    TotalSegmentator - segmentation of 104 anatomical structures in CT images.
    """

    name = "totalsegmentator-aide"
    description = "Robust segmentation of 104 anatomical structures in CT images"
    version = "0.2.0"

    def compose(self):
        """Operators go in here
        """

        logging.info(f"Begin {self.compose.__name__}")

        loader = DICOMDataLoaderOperator(self)
        selector = DICOMSeriesSelectorOperator(self,rules=Rules_Text, all_matched=True)
        to_volume = DICOMSeriesToVolumeOperator(self)
        # DICOM to NIfTI operator
        dcm2nii_op = Dcm2NiiOperator(self,output_folder="/home/hinge/Projects/medical-mcp/output")

        # # TotalSegmentator segmentation
        # totalsegmentator_op = TotalSegmentatorOperator(self)

        # # RT Struct Writer operator
        # custom_tags = {"SeriesDescription": "AI generated image, not for clinical use."}
        # rtstructwriter_op = RTStructWriterOperator(self)

        # # PDF generator
        # pdf_generator = ClinicalReviewPDFGenerator(self)

        # # Dicom encapsulation
        # model_info = ModelInfo(creator="", name="", version="", uid="")
        # #custom_tags = {"Modality": "DOC"}
        # dicom_encapsulation = DICOMEncapsulatedPDFWriterOperator(self,output_folder = "/home/hinge/Projects/medical-mcp/output", copy_tags=True,
        #                                                          model_info=model_info,
        #                                                          custom_tags=custom_tags)

        # Operator pipeline
        self.add_flow(loader, selector, {("dicom_study_list", "dicom_study_list")})

        self.add_flow(selector, to_volume, {("study_selected_series_list", "study_selected_series_list")})
        self.add_flow(to_volume, dcm2nii_op, {("image", "image")})
        
        #self.add_flow(dcm2nii_op, totalsegmentator_op, {("nii_ct_dataset", "nii_ct_dataset")})

        # self.add_flow(dcm2nii_op, rtstructwriter_op, {("dcm_input", "dcm_input")})
        # self.add_flow(totalsegmentator_op, rtstructwriter_op, {("nii_seg_output_path", "nii_seg_output_path")})

        # self.add_flow(selector, pdf_generator, {("study_selected_series_list", "study_selected_series_list")})
        # self.add_flow(dcm2nii_op, pdf_generator, {("nii_ct_dataset", "nii_ct_dataset")})
        # self.add_flow(totalsegmentator_op, pdf_generator, {("nii_seg_output_path", "nii_seg_output_path")})

        # self.add_flow(selector, dicom_encapsulation, {("study_selected_series_list", "study_selected_series_list")})
        # self.add_flow(pdf_generator, dicom_encapsulation, {("pdf_file", "pdf_file")})

        logging.info(f"End {self.compose.__name__}")

Rules_Text = """
{
    "selections": [
        {
            "name": "CT Series",
            "conditions": {
                "Modality": "CT"
            }
        }
    ]
}
"""

if __name__ == "__main__":
    TotalSegmentatorApp().run()