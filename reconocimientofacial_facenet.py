import face_recognition

known_img = face_recognition.load_image_file("empleado1.jpg")
unknown_img = face_recognition.load_image_file("entrada_actual.jpg")

known_enc = face_recognition.face_encodings(known_img)[0]
unknown_enc = face_recognition.face_encodings(unknown_img)[0]

results = face_recognition.compare_faces([known_enc], unknown_enc)
if results[0]:
    print("Acceso autorizado: rostro verificado")
else:
    print("Acceso denegado: rostro no coincide")
