default:

SOURCE ?= src
TARGET ?= dest

# get filelist
# generate md5sums
filelist:
	find ${SOURCE}/recup_dir.* > ${SOURCE}/filelist.txt
	cat ${SOURCE}/filelist.txt | xargs md5sum -b > ${SOURCE}/sums.txt

# generate metadata
out:
	cat ${SOURCE}/sums.txt | python3 check.py > ${SOURCE}/out.txt

pictures:
	cat ${SOURCE}/out.txt | python3 export.py pic ${TARGET}

music:
	cat ${SOURCE}/out.txt | python3 export.py music ${TARGET}

other:
	cat ${SOURCE}/out.txt | python3 export.py other ${TARGET}

doc:
	cat ${SOURCE}/out.txt | python3 export.py doc ${TARGET}

movie:
	cat ${SOURCE}/out.txt | python3 export.py movie ${TARGET}

music_tag:
	find ${TARGET}/Music -type f | sort | python3 tags.py ${SOURCE}/music_files.csv

music_rename:
	python3 music_tags.py ${SOURCE}/music_files.csv ${TARGET}/X
