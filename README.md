1. Start the orthanc container
2. (if first time) sh orthanc/upload_data.sh



Change the ORTHANC_IP in the monai-deploy/.env file
Likewise change the  "DicomModalities": "MONAI-DEPLOY": IP to match the monai-deploy


This will send CT series to MONAI-DEPLOY
movescu -S  -aec ORTHANC localhost 4242 -aem MONAI-DEPLOY  -k QueryRetrieveLevel=SERIES -k PatientID=Anon001 -k StudyInstanceUID= -k Modality= -k SeriesInstanceUID=2.25.277176293157759780141760041699188966257