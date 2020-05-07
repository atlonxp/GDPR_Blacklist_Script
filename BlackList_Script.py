from zipfile import ZipFile
import csv

none_found_flag = True
Blacklist_sha256 = ("2fe33383fc920edfe6fcaee21bcf503035370bb59b3a1e0c1132f09a8ef2ad43",
                    "10ca990164b990cd12f0622caa8afe7869bdf2155601bf5eac0f6ced91261b73",
                    "2fe33383fc920edfe6fcaee21bcf503035370bb59b3a1e0c1132f09a8ef2ad43",
                    "10ca990164b990cd12f0622caa8afe7869bdf2155601bf5eac0f6ced91261b73",
                    "d803bb2eb7203665c3926fb046b57e4a62cce6e6ee931a146402e3fda9d0e5be",
                    "634751ad8596c35d825e60dae8337afbe774f2a98123321510d108ac2631a07c",
                    "108dc9de876d585eb73bf9dbe8233331fe941a423ff714f60af8c983064b5a10",
                    "73be8f744f14cb92271e4013c600bf84e70b99f6144e6e753d7f181dcef05cf7",
                    "1798b32382f5db3671318ab116b3d886b71f291bbedd5824c3afd350ce0eb768",
                    "08f806690974fdbb13a30e9b80e6bdfd8e000019d506e08754c88f06f800695c",
                    "a62620c155baa9fdb5566d2ee11b51084283e53e5d59ccbb30d38ffe50c5744c")

zip_file_name = "GDPR_test.zip"

with ZipFile(zip_file_name, 'r') as zip_container_file:
    list_of_zips = zip_container_file.namelist()

    for every_zip_file in list_of_zips:
        temp_zip_file = zip_container_file.extract(every_zip_file)

        with ZipFile(every_zip_file, 'r') as zip1:
            # zip1.printdir()
            list_of_files = zip1.namelist()
            # print("List of Files: ", list_of_files)

            for item in list_of_files:
                if '-emails-only.csv' in item:
                    # print(item)

                    emailFile = zip1.extract(item)
                    with open(emailFile, 'r') as csv_file:
                        reader = csv.reader(csv_file, delimiter=',')
                        for row in reader:
                            # print(row)
                            for hash_email in Blacklist_sha256:
                                if hash_email in row:
                                    none_found_flag = False
                                    print("<-Found:->", hash_email,
                                          "<-in file:->", item,
                                          "<-from zip:->", every_zip_file)
                                    text_file = open("found_records", "a")
                                    text_file.write(
                                        "<-Found:->" + hash_email +
                                        "<-in file:->" + item +
                                        "<-from zip:->" + every_zip_file
                                    )

    if none_found_flag:
        print("no matching records.")
