@echo off

echo file: %1

certutil -encode %1 %1_encoded.txt
