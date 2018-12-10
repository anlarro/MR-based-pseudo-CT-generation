#!/bin/sh

#(fixed)mrT1SE-MRT2(moving) registration
arr1=(*_mrT1SE.nii)
arr2=(*_mrT2.nii)

for n in `seq 0 1 $((${#arr1[@]}-1))` 
do
	mkdir -p ./MRT2_reg/$n
	elastix -f ./${arr1[$n]} -m ./${arr2[$n]} -out ./MRT2_reg/$n -p ./MR-MR.txt
done


#(fixed)MRT1SE-mrT1 (MPRAGE)(moving) registration
arr3=(*_mrT1.nii)
for n in `seq 0 1 $((${#arr1[@]}-1))` 
do
	mkdir -p ./MRT1_reg/$n
	elastix -f ./${arr1[$n]} -m ./${arr3[$n]} -out ./MRT1_reg/$n -p ./MR-MR.txt
done

#(fixed)MRT1SE-CT(moving) registration
arr4=(*_ct_tra.nii)
for n in `seq 0 1 $((${#arr1[@]}-1))` 
do
	mkdir -p ./CT_tra_reg/$n
	elastix -f ./${arr1[$n]} -m ./${arr4[$n]} -out ./CT_tra_reg/$n -p ./CT-MR.txt
done




#rename results
sed -i 's/_.*/_ct_tra_reg.nii/g' list_of_patients.txt
for n in `seq 0 1 $((${#arr1[@]}-1))` 
do
	read line
	cp -v "./CT_tra_reg/$n/result.0.nii" "${line}"
done < list_of_patients.txt


sed -i 's/_.*/_mrT2_reg.nii/g' list_of_patients.txt
for n in `seq 0 1 $((${#arr1[@]}-1))` 
do
	read line
	cp -v "./MRT2_reg/$n/result.0.nii" "${line}"
done < list_of_patients.txt



sed -i 's/_.*/_mrT1_reg.nii/g' list_of_patients.txt
for n in `seq 0 1 $((${#arr1[@]}-1))` 
do
	read line
	cp -v "./MRT1_reg/$n/result.0.nii" "${line}"
done < list_of_patients.txt







elastix -f ./70193244_mrT1.nii -m ./70193244_ct_cor -out ./CT_cor_reg/23 -p ./CT-MR.txt -t0 ./CT_sag_reg/23/TransformParameters.0.txt



