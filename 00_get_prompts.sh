#!/bin/bash

. locations.conf

HERE=`pwd`


ls -1 | egrep '^..\_..(\_..\_..)?$' | while read LNG; do

    
    echo "$LNG"

    mkdir -p $LNG

    cd $HERE/$LNG

    # Do we have common voice?

    CORPUS=${LNG}_COMMON_VOICE_DIR
    #echo $CORPUS
    #echo ${!CORPUS}
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS"
		for collection in train dev test; do
		    #echo "    Trying to read ${!CORPUS}/${collection}.tsv"
		    tail -n +1 ${!CORPUS}/${collection}.tsv | cut -f 2,3 | tr '[\t]' '[ ]'
		done | sort -u > ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    # Do we have PF-STAR?

    CORPUS=${LNG}_PFSTAR_DIR
    #echo $CORPUS
    #echo ${!CORPUS}
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS"
		for collection in train test eval; do
		    #echo "    Trying to read ${!CORPUS}/${collection}.tsv"
		    #tail -n +1 ${!CORPUS}/${collection}.trn | rev | cut -f 2- -d ' ' | rev
		    cat ${!CORPUS}/${collection}.trn | sed -r 's/(.*) \((.*)\)/\2 \1/g'
		done | sort -u > ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi
    
    

    # Do we have WSJCAM?

    CORPUS=${LNG}_WSJCAM0_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS"
		if [ ! -s ${CORPUS}-dotfilelist.txt ]; then 
		    find ${!CORPUS}/Disk*/wsjcam0/*/*/*.dot > ${CORPUS}-dotfilelist.txt
		fi
		cat ${CORPUS}-dotfilelist.txt | while read f; do cat $f | sed -r 's/(.*) \((.*)\)/\2 \1/g'; done | sort -u > ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi
    
    CORPUS=${LNG}_SIAK_FI_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS"
		if [ ! -s ${CORPUS}-audiofilelist.txt ]; then
		    #echo "    Trying to read ${!CORPUS}/${collection}.tsv"
		    find ${!CORPUS}/game_data_201706/wav_ok/  ${!CORPUS}/game_data_201806/wav_ok/ -name "*.wav"  > ${CORPUS}-audiofilelist.txt
		fi
		# Filenames are of the form:
		# ylinemi_193_cucumber_20170427-082519-707
		# ylinemi_271_living_room_20170503-120347-398
		cat ${CORPUS}-audiofilelist.txt | sed -r 's/.*\///' | sed -r 's/(.*\_[0-9]+\_)([a-z\_]+)(\_20[0-9\-]+)\.wav/\1\2\3 \2/g' | sed -r 's/\_txt$//g' | sed -r -e 's/ ([a-z]+)\_/ \1 /g' -e 's/ ([a-z]+)\_/ \1 /g' -e 's/ ([a-z]+)\_/ \1 /g' -e 's/ ([a-z]+)\_/ \1 /g' -e 's/ ([a-z]+)\_/ \1 /g' -e 's/ ([a-z]+)\_/ \1 /g' -e 's/ ([a-z]+)\_/ \1 /g' -e 's/ ([a-z]+)\_/ \1 /g' -e 's/ ([a-z]+)\_/ \1 /g'| sort -u > ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi

	fi
    fi

    CORPUS=${LNG}_SIAK_KINDERGARTEN_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS"
		if [ ! -s ${CORPUS}-audiofilelist.txt ]; then
		    #echo "    Trying to read ${!CORPUS}/${collection}.tsv"
		    find ${!CORPUS}/split_batch1/long_filenames/ -name *.wav | grep 'fi_fi' > ${CORPUS}-audiofilelist.txt
		fi
		cat ${CORPUS}-audiofilelist.txt |  sed -r 's/.*\/(.*\-)([a-z_]+)(\.wav)/\1\2\3 \2/g' | sed -r -e 's/ fi\_fi\_/ /g' -e 's/ ([a-zäö]*)\_/ \1 /g'  -e 's/ ([a-zäö]*)\_/ \1 /g' -e 's/ ([a-zäö]*)\_/ \1 /g' -e 's/ ([a-zäö]*)\_/ \1 /g' -e 's/ ([a-zäö]*)\_/ \1 /g' -e 's/ ([a-zäö]*)\_/ \1 /g'  -e 's/ ([a-zäö]*)\_/ \1 /g'  -e 's/ ([a-zäö]*)\_/ \1 /g' |  sort -u > ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    CORPUS=${LNG}_SIAK_KINDERGARTEN_L2_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS"
		if [ ! -s ${CORPUS}-audiofilelist.txt ]; then
		    #echo "    Trying to read ${!CORPUS}/${collection}.tsv"
		    #find ${!CORPUS}/split_batch1/short_filenames/ -name *.wav | grep -v suomi > ${CORPUS}-audiofilelist.txt
		    find ${!CORPUS}/split_batch1/long_filenames/ -name *.wav | grep -v 'fi_fi' > ${CORPUS}-audiofilelist.txt
		fi
		cat ${CORPUS}-audiofilelist.txt |  sed -r 's/.*\/(.*\-)([a-z_]+)(\.wav)/\1\2\3 \2/g' | sed -r -e 's/ en\_uk\_/ /g' -e 's/ en\_uk\_/ /g' -e 's/ en\_uk\_/ /g' | sort -u > ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    

    
    # Do we have WSJ?

    CORPUS=${LNG}_WSJ0_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 

	    echo "  - Collecting prompts from $CORPUS"
	    if [ ! -s ${CORPUS}-dotfilelist.txt ]; then
		cat ${!CORPUS}/dot_files.txt | awk '{print "'${!CORPUS}/'" $1}' > ${CORPUS}-dotfilelist.txt 
		find ${!CORPUS}/*_et_*/ -name *.dot >> ${CORPUS}-dotfilelist.txt
	    fi
	    cat ${CORPUS}-dotfilelist.txt | while read f; do cat $f | sed -r 's/(.*) \((.*)\)/\2 \1/g'; done | sort -u > ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    CORPUS=${LNG}_WSJ1_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
	    echo "  - Collecting prompts from $CORPUS"
	    if [ ! -s ${CORPUS}-dotfilelist.txt ]; then 
		find ${!CORPUS}/trans/wsj1/si*/*/*.dot > ${CORPUS}-dotfilelist.txt
		find ${!CORPUS}/si_et_*/ -name *.dot >> ${CORPUS}-dotfilelist.txt
	    fi
	    cat ${CORPUS}-dotfilelist.txt | while read f; do cat $f | sed -r 's/(.*) \((.*)\)/\2 \1/g'; done | sort -u > ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    CORPUS=${LNG}_TIDIGITS_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
	    echo "  - Collecting prompts from $CORPUS"
	    if [ ! -s ${CORPUS}-audiofilelist.txt ]; then
		#echo "    Trying to read ${!CORPUS}/${collection}.tsv"
		find ${!CORPUS}/data/children/*/*/*/*.wav > ${CORPUS}-audiofilelist.txt
	    fi
	    cat ${CORPUS}-audiofilelist.txt | sed -r 's/.*\/([0-9oz]+)([ab]?\.wav)$/\1/g' \
		| sed -r 's/o/oh /g' \
		| sed -r 's/z/zero /g' \
		| sed -r 's/1/one /g' \
		| sed -r 's/2/two /g' \
		| sed -r 's/3/three /g' \
		| sed -r 's/4/four /g' \
		| sed -r 's/5/five /g' \
		| sed -r 's/6/six /g' \
		| sed -r 's/7/seven /g' \
		| sed -r 's/8/eight /g' \
		| sed -r 's/9/nine /g' > ${CORPUS}-utterances.txt
	    cat ${CORPUS}-audiofilelist.txt | sed -r 's/.*\///' | paste -d ' ' - ${CORPUS}-utterances.txt > ${CORPUS}-sentences.txt 
		# ADD SOMETHING HERE | sort -u > ${CORPUS}-${collection}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    CORPUS=${LNG}_CSLU_KIDS_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS"
		#cut -f 2- -d ' ' ${!CORPUS}/aalto_extras/lists/prompts_* | sort -u > ${CORPUS}-sentences.txt
		cat ${!CORPUS}/aalto_extras/lists/prompts_* | sort -u > ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    # Do we have Spraakbanken (Swedish)?
    CORPUS=${LNG}_SPRAAKBANKEN_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS"
		#cut -f 2- -d ' ' ${!CORPUS}/transcriptions/spraakbanken_se_all_lab.txt | sort -u > ${CORPUS}-sentences.txt
		cat ${!CORPUS}/transcriptions/spraakbanken_se_all_lab.txt | sort -u > ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    
    # Do we have Speecon-Fi?

    CORPUS=${LNG}_SPEECON_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS"
		tail -n +2 ${!CORPUS}/CONTENT0.LST | cut -f 9- | sort -u | iconv -f 'iso-8859-15' -t 'utf-8' > ${CORPUS}-utterances.txt
		tail -n +2 ${!CORPUS}/CONTENT0.LST | cut -c 26-33 | paste -d ' ' - ${CORPUS}-utterances.txt >  ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    CORPUS=${LNG}_SPEECONKIDS_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then 
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS"
		tail -n +2 ${!CORPUS}/CONTENT0.LST | cut -f 9- | sort -u  | iconv -f 'iso-8859-15' -t 'utf-8' > ${CORPUS}-utterances.txt
		tail -n +2 ${!CORPUS}/CONTENT0.LST | cut -c 26-33 | paste -d ' ' - ${CORPUS}-utterances.txt >  ${CORPUS}-sentences.txt 
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    CORPUS=${LNG}_TELLME_AR_DIR
    if [ "${!CORPUS}" != "" ]; then
	if [ -d "${!CORPUS}" ]; then
	    if [ ! -s ${CORPUS}-sentences.txt ]; then 
		echo "  - Collecting prompts from $CORPUS (the awkward grep...)"
		#cut -f 2- ${!CORPUS}/prompt_to_words.txt > ${CORPUS}-sentences.txt 
		#cat ${!CORPUS}/prompt_to_words.txt > ${CORPUS}-sentences.txt
		grep renamed_wanhat ${!CORPUS}/scorings/aino/audio_that_was_rated/filelist.txt | sed -r 's/.*\/(.*)\.wav/\1/g' > ${CORPUS}-filelist1.txt
		cat ${CORPUS}-filelist1.txt | rev | cut -f 1 -d '_' | rev | cut -f 1 -d '.' | while read l; do egrep -m1 "^$l " ${!CORPUS}/prompt_to_words.txt | cut -f 2- -d ' '; done > ${CORPUS}-utterances1.txt
		
		grep -v renamed_wanhat ${!CORPUS}/scorings/aino/audio_that_was_rated/filelist.txt | sed -r 's/.*\/(.*)\.wav/\1/g' > ${CORPUS}-filelist2.txt
		cat ${CORPUS}-filelist2.txt | sed -r 's/.*\///' | cut -f 3- -d '_' | rev | cut -f 2- -d '_' | rev | while read l; do egrep -m1 "^$l " ${!CORPUS}/prompt_to_words.txt | cut -f 2- -d ' '; done > ${CORPUS}-utterances2.txt

		paste ${CORPUS}-filelist1.txt ${CORPUS}-utterances1.txt > ${CORPUS}-sentences.txt
		paste ${CORPUS}-filelist2.txt ${CORPUS}-utterances2.txt >> ${CORPUS}-sentences.txt
	    else
		echo "  - ${CORPUS} already processed"
	    fi
	fi
    fi

    
    cat *-sentences.txt > all_sentences.txt
    #cat all_sentences.txt | tr '[ ]' '[\n]' | sort -u > all_words.txt
    
done
