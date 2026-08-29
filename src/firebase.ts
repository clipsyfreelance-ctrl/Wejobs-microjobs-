import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAgy5vl0v8i4xrORRG1iFcu61--JR40q6s",
  authDomain: "wejobs-app.firebaseapp.com",
  projectId: "wejobs-app",
  storageBucket: "wejobs-app.firebasestorage.app",
  messagingSenderId: "570876121705",
  appId: "1:570876121705:web:fe4256cbd7cfc2b1488f8",
  measurementId: "G-G7WGP7MQVY"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
