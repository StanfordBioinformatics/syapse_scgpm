import syapse_scgpm	

def getControlLibraryForExpLibraryOnChipSs(library_uid):
	query = """
		SELECT ?Library_D.sys:uniqueId WHERE {
    REQUIRE PATTERN ?ScgpmFSnapScoring_A enc:ScgpmFSnapScoring {
        enc:hasExperimentToControl ?ExperimentToControl_B .
        PATTERN ?ExperimentToControl_B enc:ExperimentToControl {
            enc:hasExperimentalLibrary ?Library_C .
            enc:hasControlLibrary ?Library_D
        }
    }
    PATTERN ?Library_C enc:Library {
        sys:uniqueId """ + "'" + library_uid + "'" + """
    }
    PATTERN ?Library_D enc:Library {}
	}
	LIMIT 20
	"""
	return query

def getEncffNumberOnLibrary(library_uid,forwardRead=True):
	if forwardRead:
		read = "1"
	else:
		read = "2"
	query = """
		SELECT ?dccfileinfo_C.enc:encffNumber WHERE {
    REQUIRE PATTERN ?Library_A enc:Library {
        sys:uniqueId """ + "'" + library_uid + "'" + """ .
        enc:hasDcc_file_info ?dccfileinfo_C .
        PATTERN ?dccfileinfo_C enc:dccfileinfo {
            EXISTS enc:encffNumber  .
            enc:hasPaired_end """ + "'" + read + "'" + """
        }
    }
	}
	LIMIT 20
	"""
	return query


def getEncffNumberOnAtacSeq(atacseq_uid,forwardRead=True):
	if forwardRead:
		read = "1"
	else:
		read = "2"

	query = """
		SELECT ?dccfileinfo_B.enc:encffNumber WHERE {
    REQUIRE PATTERN ?AtacSeq_A enc:AtacSeq {
        sys:uniqueId """ + "'" + atacseq_uid + "'" + """ .
        enc:hasDcc_file_info ?dccfileinfo_B .
        PATTERN ?dccfileinfo_B enc:dccfileinfo {
            EXISTS enc:encffNumber  .
            enc:hasPaired_end """ + "'" + read + "'" + """
        }
    }
	}
	LIMIT 20
	"""
	return query	

def getLibraryWithDccUuid(dcc_uuid):
	query = """
		SELECT ?Library_A.sys:uniqueId WHERE {
    	REQUIRE PATTERN ?Library_A enc:Library {
        enc:dcc_library_uuid """ + "'" + dcc_uuid + "'" + """
    }
	}
	LIMIT 20
	"""
	return query

def getAtacSeqWithDccUuid(dcc_uuid):
	query = """
		SELECT ?AtacSeq_A.sys:uniqueId WHERE {
    REQUIRE PATTERN ?AtacSeq_A enc:AtacSeq {
        enc:dcc_library_uuid """ + "'" + dcc_uuid + "'" + """
    }
	}
	LIMIT 20
	"""
	return query

def getChipWithLibrary(library_uid):
	query = """
		SELECT ?ScgpmDChIP_A.sys:uniqueId WHERE {
    REQUIRE PATTERN ?ScgpmDChIP_A enc:ScgpmDChIP {
        enc:hasBioSampleLink/enc:hasLibrary ?Library_C
    }
    PATTERN ?Library_C enc:Library {
        sys:uniqueId """ + "'" + library_uid + "'" + """
 	   }
	}
	LIMIT 20
	"""
	return query

def getSeqResForLibrary(library_uid):
	query = """
		SELECT ?EncodeSequencingResults_A.sys:uniqueId WHERE {
   	 REQUIRE PATTERN ?EncodeSequencingResults_A enc:EncodeSequencingResults {
   	     enc:hasLibrary ?Library_B
   	 }
   	 PATTERN ?Library_B enc:Library {
   	     sys:uniqueId """ + "'" + library_uid + "'" + """
   	 }
	}
	LIMIT 20
	"""
	return query


def getSeqResForAtacSeq(atacseq_uid):
	query = """
		SELECT ?EncodeSequencingResults_B.sys:uniqueId WHERE {
    REQUIRE PATTERN ?AtacSeq_A enc:AtacSeq {
        sys:uniqueId """ + "'" + atacseq_uid + "'" + """ .
        REVERSE enc:EncodeSequencingResults ?EncodeSequencingResults_B
    }
    PATTERN ?EncodeSequencingResults_B enc:EncodeSequencingResults {}
	}
	LIMIT 20
	"""
	return query

def getSeqReqForLibrary(library_uid):
	query = """
		SELECT ?SequencingRequest_A.sys:uniqueId WHERE {
    REQUIRE PATTERN ?SequencingRequest_A enc:SequencingRequest {
        enc:hasLibrary ?Library_B
    }
    PATTERN ?Library_B enc:Library {
        sys:uniqueId """ + "'" + library_uid + """
    }
	}
	LIMIT 20
	"""
	return query

def getAntibodyUidFromLibrary(library_uid):
	"""
	Function : Gets the unique ID of the Antibody (ScgpmBAntibodySelection) on the Library object.
	Args     : library_uid - The syapse unique ID for a Library or AtacSeq object.
	Returns  : str. 
	"""
	query = """
		SELECT ?ScgpmBAntibodySelection_B.sys:uniqueId WHERE {
   	 REQUIRE PATTERN ?Library_A enc:Library {
   	     sys:uniqueId """ + "'" + library_uid + "'" + """ .
   	     enc:hasScgpmBAntibodySelection ?ScgpmBAntibodySelection_B
   	 }
   	 PATTERN ?ScgpmBAntibodySelection_B enc:ScgpmBAntibodySelection {}
		}
		LIMIT 20
	"""
	return query

def getSeqResFromSeqReq_library(sreq_id,lims_barcode):
	"""
	Function : Gets the sequencing result(s) for a particular sequencing request and barcode combination. 
	Args     : sreq_id
	Returns  : tuple. contains two items of the form [SequencingResult_uid,Library_uid].
	"""
	query = """
		SELECT ?EncodeSequencingResults_C.sys:uniqueId ?Library_B.sys:uniqueId WHERE {
    REQUIRE PATTERN ?SequencingRequest_A enc:SequencingRequest {
        sys:uniqueId """ + "'" + sreq_id + "'" + """ .
        enc:hasLibrary ?Library_B
    }
    PATTERN ?Library_B enc:Library {
        REVERSE enc:EncodeSequencingResults ?EncodeSequencingResults_C .
        REVERSE enc:ScgpmDChIP ?ScgpmDChIP_D
    }
    PATTERN ?EncodeSequencingResults_C enc:EncodeSequencingResults {}
    PATTERN ?ScgpmDChIP_D enc:ScgpmDChIP {
        enc:hasBioSampleLink ?BioSampleLink_E .
        PATTERN ?BioSampleLink_E enc:BioSampleLink {
            enc:hasLibrary ?Library_B .
            enc:barcode """ + "'" + lims_barcode + "'" + """
        }
	    }
	}
	LIMIT 20
	"""
	return query


def getSeqResFromSeqReq_atacSeq(sreq_id,lims_barcode):
	"""
	Function : Gets the sequencing result(s) for a particular sequencing request and barcode combination. 
	Args     : sreq_id
	Returns  : tuple. contains two items of the form [SequencingResult_uid,Library_uid].
	"""
	query = """
		SELECT ?EncodeSequencingResults_D.sys:uniqueId ?AtacSeq_C.sys:uniqueId WHERE {
    	REQUIRE PATTERN ?SequencingRequest_A enc:SequencingRequest {
     	   sys:uniqueId """ + "'" + sreq_id + "'" + """ .
     	   enc:hasAtacSeq ?AtacSeq_C
   	 }
   	 PATTERN ?AtacSeq_C enc:AtacSeq {
   	     REVERSE enc:EncodeSequencingResults ?EncodeSequencingResults_D .
   	     enc:barcode """ + "'" + lims_barcode + "'" + """
   	 }
   	 PATTERN ?EncodeSequencingResults_D enc:EncodeSequencingResults {}
	}
	LIMIT 20
	"""
	return query


def getBiosampleUidFromAtacSeqLibrary(library_uid):
	"""
	Function :
	"""
	query = """
		SELECT ?BiosampleENTex_B.sys:uniqueId WHERE {
 	   REQUIRE PATTERN ?AtacSeq_A enc:AtacSeq {
 	       sys:uniqueId """ + "'" + library_uid + "'" + """ .
 	       enc:hasBiosampleENTex ?BiosampleENTex_B
  	  }
   	 PATTERN ?BiosampleENTex_B enc:BiosampleENTex {}
		}
		LIMIT 20
	"""
	return query

def getBiosampleUidFromLibrary(library_uid):

	query = """
		SELECT ?ScgpmBiosample_D.sys:uniqueId WHERE {
    REQUIRE PATTERN ?Library_A enc:Library {
        sys:uniqueId """ + "'" + library_uid + "'" + """ .
        REVERSE enc:ScgpmDChIP ?ScgpmDChIP_B
    }
    PATTERN ?ScgpmDChIP_B enc:ScgpmDChIP {
        enc:hasBioSampleLink ?BioSampleLink_C .
        PATTERN ?BioSampleLink_C enc:BioSampleLink {
            enc:hasLibrary ?Library_A .
            enc:hasBiosample ?ScgpmBiosample_D
        }
    }
    PATTERN ?ScgpmBiosample_D enc:ScgpmBiosample {}
		}
		LIMIT 20
		"""
	return query

def getWesternBlotsToSubmit():
	"""
	Function : The corresponding saved query name on Syapse is called WB_AB_Char_SySQL. This query finds all Wester Blots 
						 that have an antibody selection, secondary validation, and status of "Send to DCC".
	Returns  : str. The Syapse SyQL query.
	"""
	query = """
		SELECT ?ScgpmBWesternBlot_A.sys:uniqueId ?AntibodyTested_B.enc:rowNumWB ?ScgpmBAntibodySelection_C.sys:uniqueId ?ScgpmSecondaryAntibody_D.sys:uniqueId WHERE {
			REQUIRE PATTERN ?ScgpmBWesternBlot_A enc:ScgpmBWesternBlot {
				enc:hasAntibodyTested ?AntibodyTested_B .
				PATTERN ?AntibodyTested_B enc:AntibodyTested {
					enc:hasScgpmBAntibodySelection ?ScgpmBAntibodySelection_C .
					enc:hasSecondaryScgpmBAntibodySelection ?ScgpmSecondaryAntibody_D .
					enc:submittedToDcc 'Send to DCC'
				}
			}
  		PATTERN ?ScgpmBAntibodySelection_C enc:ScgpmBAntibodySelection {}
  		PATTERN ?ScgpmSecondaryAntibody_D enc:ScgpmSecondaryAntibody {}
		} 
		LIMIT 20000
		"""
	return query

def getLibraryLinkOnSequencingRequest(seq_req_suid, barcode):
	"""  
	Function :  Retrieves the app_ind_id of the library that is linked to the seq_req_suid and has the given barcode.
							Recall that a ChIP object typically has 6 ChIP experiments (see ChIP-1073 in Syapse for an example). This is a saved
							query on Syapse, named getLibraryAndBarcodeAssociationsOnSeqRequest.
	Args     : 
	Returns  :  Returns  : str. The Syapse SyQL query.
	"""
	library = None 
	##Fix the 'sample run name' to remove the rcvd ##/##/####
	seq_req_suid = seq_req_suid.split()[0]
	query = """
			SELECT ?SequencingRequest_A.sys:name ?SequencingRequest_A.sys:uniqueId ?Library_B.sys:name ?Library_B.sys:uniqueId ?ScgpmDChIP_C.sys:name ?ScgpmDChIP_C.sys:uniqueId ?BioSampleLink_I.enc:barcode WHERE {
			    REQUIRE PATTERN ?SequencingRequest_A enc:SequencingRequest {
			        sys:uniqueId """ + "'" + seq_req_suid + "'" + """ .
			        enc:hasLibrary ?Library_B
			    }
			    PATTERN ?Library_B enc:Library {
			        REVERSE enc:ScgpmDChIP ?ScgpmDChIP_C
			    }
			    PATTERN ?ScgpmDChIP_C enc:ScgpmDChIP {
			        enc:hasBioSampleLink ?BioSampleLink_I .
			        PATTERN ?BioSampleLink_I enc:BioSampleLink {
			            enc:hasLibrary ?Library_B .
			            enc:barcode """ + "'" + barcode + "'" + """
			        }
			    }
			}
			LIMIT 200
"""
	return query

	#[0] - SEQUENCING REQUEST: A   RECORD NAME 
	#[1] - SEQUENCING REQUEST: A   UNIQUE ID 
	#[2] - LIBRARY: B  RECORD NAME 
	#[3] - LIBRARY: B  UNIQUE ID 
	#[4] - CHIP: C   RECORD NAME 
	#[5] - CHIP: C   UNIQUE ID 
	#[6] - BIOSAMPLELINK: D  LIBRARY
	#[7] - BIOSAMPLELINK: D  BARCODE

	return query


def atacSeq_getLibraryLinkOnSequencingRequest(seq_req_suid, barcode):
	"""
	Function :
	Args     : seq_req_suid - 
						 barcode      -
	Returns  : str. The Syapse SyQL query.
	Ex:      : atac_getLibraryLinkOnSequencingRequest(seq_req_suid="SReq-937",barcode="16:TCCTGAGC")
	"""

	query = """
		SELECT ?SequencingRequest_A.sys:name ?SequencingRequest_A.sys:uniqueId ?AtacSeq_C.sys:name ?AtacSeq_C.sys:uniqueId WHERE {
    REQUIRE PATTERN ?SequencingRequest_A enc:SequencingRequest {
        sys:uniqueId """ + "'" + seq_req_suid + "'" + """ . 
        enc:hasAtacSeq ?AtacSeq_C
    }
    PATTERN ?AtacSeq_C enc:AtacSeq {
        enc:barcode """ + "'" + barcode + "'" + """
    }
}
LIMIT 20
	"""
	return query

def getBiosamplesWithoutDccStatusSet():
	"""
	Function : Queries all Biosamples of type biosample (and not ENTex biosamples, for example) that don't yet have a DCC Status field.
             This is useful if one needs to set the DCC Status field to something like Send to DCC.
	Returns  : str. The Syapse SyQL query.
	"""
	query = """
		SELECT ?ScgpmBiosample_A.sys:uniqueId WHERE {
			REQUIRE PATTERN ?ScgpmBiosample_A enc:Biosample {
				NOT enc:hasDccField ?DccField_B .
				PATTERN ?DccField_B enc:DccField {}
    	}
		}
		LIMIT 2000
		"""
	return query

def getSeqRequestsWithoutSeqResultsQuery():
	"""
	Function : Queries all Sequencing Request (SReq) objects to check whether the barcode libraries of the Library object type all have a Sequencing Result (SRes) object. Each
               result returned by the query will contain the SReq unique ID. Essentially, if any of the library objects reference on the sequencing request object don't have
               a SRes object, then the SReq object label will be included in this query's results.
	Return   : str. The Syapse SyQL query.
	"""

	query = """
					SELECT ?SequencingRequest_A.sys:label WHERE {
						REQUIRE PATTERN ?SequencingRequest_A enc:SequencingRequest {
							enc:hasLibrary ?Library_B
						}
						PATTERN ?Library_B enc:Library {
							NOT EXISTS REVERSE enc:EncodeSequencingResults
						}
				}
				LIMIT 2000
				"""
	return query


def getAtacSeqSeqRequestsWithoutSeqResultsQuery():
	"""
	Function : Queries all Sequencing Request (SReq) objects to check whether the barcode libraries of the AtacSeq library object type all have a Sequencing Result (SRes) object. Each
               result returned by the query will contain the SReq unique ID. Essentially, if any of the library objects reference on the sequencing request object don't have
               a SRes object, then the SReq object label will be included in this query's results.
	Return   : str. The Syapse SyQL query.
	"""

	query = """
					SELECT ?SequencingRequest_A.sys:label WHERE {
	    			REQUIRE PATTERN ?SequencingRequest_A enc:SequencingRequest {
	        		enc:hasAtacSeq ?AtacSeq_C
	    			}
	    			PATTERN ?AtacSeq_C enc:AtacSeq {
	        		NOT EXISTS REVERSE enc:EncodeSequencingResults
	    			}
				}
				LIMIT 2000
				"""
	return query

def getBarcodesOnSeqRequestQuery(seq_req_uid):
	"""
	Function : Given a Sequencing Request object ID from Syapse, gives the query needed to fetch all Barcodes associated on that Sequencing Request.
	Args     : seq_req_uid - str. A Sequencing Request object ID from Syapse.
	Returns  : str. The Syapse SyQL query.

	Table Columns:
	[0] - Syapse Library - Link
	[1] - Syapse Unique ID for Library
	[2] - Barcode for the Library
	[3] - Sequencing Platform
	"""
	query = """
					SELECT ?BioSampleLink_E.enc:hasLibrary ?Library_B.sys:uniqueId ?BioSampleLink_E.enc:barcode 
					?SequencingRequest_A.enc:sequencingPlatform WHERE {
					    REQUIRE PATTERN ?SequencingRequest_A enc:SequencingRequest {
					        enc:hasLibrary ?Library_B .
					        sys:uniqueId """ + "'" + seq_req_uid + "'"  + """
					    }
					    PATTERN ?Library_B enc:Library {
					        REVERSE enc:ScgpmDChIP ?ScgpmDChIP_D
					    }
					    PATTERN ?ScgpmDChIP_D enc:ScgpmDChIP {
					        enc:hasBioSampleLink ?BioSampleLink_E .
					        PATTERN ?BioSampleLink_E enc:BioSampleLink {
					            enc:hasLibrary ?Library_B
					        }
					    }
					}
					LIMIT 2000
					"""
	return query

def getBarcodeFromSeqResObj(seq_result_uid):
	"""
	Function : Fetches the barcode from a Syapse SequencingResult object.
	Args     : seq_result_uid - str. A Syapse SequencingResult UID.
	"""	
	query = """
					SELECT ?EncodeSequencingResults_A.enc:barcode WHERE {
    				REQUIRE PATTERN ?EncodeSequencingResults_A enc:EncodeSequencingResults {
        			sys:uniqueId """ + "'" + seq_result_uid + "'" + """
    				}
					}
					LIMIT 2000
					"""
	return query

def getSeqResultObjsFromSeqReqObj(app_ind_id):
	"""
	Function :
	"""
	query = """
				SELECT ?EncodeSequencingResults_A.sys:uniqueId ?Library_E.sys:uniqueId ?BioSampleLink_K.enc:barcode WHERE {
				    REQUIRE PATTERN ?EncodeSequencingResults_A enc:EncodeSequencingResults {
				        enc:hasLibrary ?Library_E
				    }
				    PATTERN ?Library_E enc:Library {
				        REVERSE enc:ScgpmDChIP ?ScgpmDChIP_F .
				        REVERSE enc:SequencingRequest """ + app_ind_id + """
				    }
				    PATTERN ?ScgpmDChIP_F enc:ScgpmDChIP {
				        enc:hasBioSampleLink ?BioSampleLink_K .
				        PATTERN ?BioSampleLink_K enc:BioSampleLink {
				            EXISTS enc:barcode  .
				            enc:hasLibrary ?Library_E
				        }
				    }
				}
				LIMIT 2000
				"""
	return query

def getScoringsWithStatus(scoringStatus,mode):
	"""
	Function : Find All ChIP Seq Scoring Objects with Scoring Status = "Awaiting Scoring". Once executed, the query will return the following fileds in the order given:
										1) ChIP Seq Scoring-UID
										2) Exp. Library-UID
										3) Exp. SRes-UID
										4) Exp. Flowcell
										5) Exp. Lane
										6) Exp. Barcode
										7) Ctl. Library-UID
										8) Ctl. SRes-UID
										9) Ctl. Flowcell
										10) Ctl. Lane
										11) Ctl. Barcode
										12) Ctl. Library-UID
	Args     : scoringStatus - One of the possible scoringStatus values of a ChipScoring object in Syapse.
						 mode - A string indicating which Syapse Host to use. Must be one of elemensts given in syapse.Syapse.knownModes.
	Returns  : str. being the query. 
	"""

	kbclassName = "ScgpmFSnapScoring"
	propertyName = "scoringStatus"
	syapse = syapse_scgpm.syapse.Syapse(mode=mode)
	rangeValues = syapse.getPropertyEnumRangeFromKbClassId(kbclass_id=kbclassName,propertyName=propertyName)
	if not scoringStatus in rangeValues:
		raise ValueError("scoringStatus must be one of {rangeValues}.".format(rangeValues=rangeValues))
	
	query = """
				SELECT ?ScgpmFSnapScoring_A.sys:uniqueId ?Library_C.sys:uniqueId ?EncodeSequencingResults_E.sys:uniqueId ?EncodeSequencingResults_E.enc:cell \
				?EncodeSequencingResults_E.enc:lane ?SequencingResultsBarcodeResults_F.enc:barcode ?Library_D.sys:uniqueId ?EncodeSequencingResults_G.sys:uniqueId \
				?EncodeSequencingResults_G.enc:cell ?EncodeSequencingResults_G.enc:lane ?SequencingResultsBarcodeResults_H.enc:barcode ?Library_D.sys:name WHERE {
				    REQUIRE PATTERN ?ScgpmFSnapScoring_A enc:ScgpmFSnapScoring {
				        enc:hasExperimentToControl ?ExperimentToControl_B .
				        PATTERN ?ExperimentToControl_B enc:ExperimentToControl {
				            enc:hasExperimentalLibrary ?Library_C .
				            enc:hasControlLibrary ?Library_D
				        } .
				        enc:scoringStatus """ +  "'{scoringStatus}' ".format(scoringStatus=scoringStatus) + """
				    }
				    PATTERN ?Library_C enc:Library {
				        REVERSE enc:EncodeSequencingResults ?EncodeSequencingResults_E
				    }
				    PATTERN ?EncodeSequencingResults_E enc:EncodeSequencingResults {
				        enc:hasSequencingResultsBarcodeResults ?SequencingResultsBarcodeResults_F .
				        PATTERN ?SequencingResultsBarcodeResults_F enc:SequencingResultsBarcodeResults {}
				    }
				    PATTERN ?Library_D enc:Library {
				        REVERSE enc:EncodeSequencingResults ?EncodeSequencingResults_G
				    }
				    PATTERN ?EncodeSequencingResults_G enc:EncodeSequencingResults {
				        enc:hasSequencingResultsBarcodeResults ?SequencingResultsBarcodeResults_H .
				        PATTERN ?SequencingResultsBarcodeResults_H enc:SequencingResultsBarcodeResults {}
				    }
				}
				LIMIT 2000
				"""

	return query

def getScoringsReady(mode):
	return getScoringsWithStatus(mode=mode,scoringStatus="Start Scoring")

def getScoringsInProgress(mode):
	return getScoringsWithStatus(mode=mode,scoringStatus="Processing Scoring Results")

def getScoringsCompleted(mode):
	return getScoringsWithStatus(mode=mode,scoringStatus="Scoring Completed")

def getScoringsFailed(mode):
	return getScoringsWithStatus(mode=mode,scoringStatus="Scoring Failed")

