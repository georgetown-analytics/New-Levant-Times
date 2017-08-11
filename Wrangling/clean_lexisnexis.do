*Gerhard Ottehenning
*7/25/2016
*Steps:
*1) Convert variables to numeric
*2) Clean string values
*3) Drop observations and variables that are not needed to sentiment analysis

*------------------------------------------------------------------------------*
*							LexisNexis csv cleaning							   *
*------------------------------------------------------------------------------*

global capstone "/Users/laurieottehenning/Documents/Georgetown Data Science /Capstone"

*1) Convert variables to numeric

import delimited "$capstone/Syria_LexisNexis.csv", varnames(1) encoding(UTF-8) clear

	**Remove all white space
		foreach var of varlist * {
			capture replace `var' = trim(`var')
			}	
	
	**Search ID
		gen test = real(search_id)
			tab search_id if test==.
			/*
				  SEARCH_ID |      Freq.     Percent        Cum.
			----------------+-----------------------------------
				   Download |         51        4.95        4.95
				   Provided |        875       84.87       89.82
			Syndigate.info, |         49        4.75       94.57
					   This |         55        5.33       99.90
					  Trend |          1        0.10      100.00
			----------------+-----------------------------------
					  Total |      1,031      100.00
		  */
		  
		destring search_id, gen(x) force
			drop search_id
			ren x search_id

	**Length
		replace length = subinstr(length, "words", "", .)
		destring length, replace
		
*2) Clean string variables

	**Publication
		replace publication = subinstr(publication, ".com", "", .)
		replace publication = itrim(publication)
		replace publication = "" if strpos(publication, "DOCUMENTS")>0
		replace publication = "BBC" if strpos(publication, "BBC")>0
		replace publication = proper(publication)
		replace publication = "BBC" if publication=="Bbc"
		replace publication = "The New York Times" if strpos(publication, "New York Times")>0
		
		levelsof publication if strpos(publication, "Guardian"), clean s(,)
			replace publication = "The Guardian" if ///
			inlist(publication, "Guardian","Guardian Weekly","Guardian.","Mail & Guardian","The Guardian","The Guardian - Final Edition")
		
	**Publication type
		replace publicationtype = proper(publicationtype)
		
	**Date
		split date, p("-")
		forvalues i=1/3 {
			destring date`i', replace
			}
		ren date1 year
		ren date2 month
		ren date3 day

*4) Split publication into dummy variables

	**Create local of publication values
		qui levelsof publication, local(pub)
		local pub: subinstr local pub "*" "_" 
		local pub: subinstr local pub " " "_"
		local pub: subinstr local pub "(" "_" 
		local pub: subinstr local pub ")" ""
		local pub: subinstr local pub "," "" 
		foreach val of local pub {
			di "`val'"
			}
			local pub: subinstr local pub " " "_" 
			local pub: subinstr local pub "." "" 
			gen `val' = 
		
*3) Drop variables

	**Drop duplications
		duplicates drop //1109 obs dropped
		duplicates drop publication date text, force
		/*
		Duplicates in terms of all variables

		--------------------------------------
		   copies | observations       surplus
		----------+---------------------------
				1 |        14828             0
		-------------------------------------- */
		
	**Drop observations
		drop if test==. //1031 obs dropped
		drop if length>20000 //1 obs dropped
		gen blank_text = 1 if text==""
			drop if blank_text==1 //1 obs dropped
		
	**Keep variables
		keep publication date title length publicationtype text year month day

sort year month day

export delimited using "$capstone/CleanLexisNexis", replace
//outsheet * using "$capstone/CleanLexisNexis.csv" , comma replace
