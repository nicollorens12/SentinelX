import React, { useEffect } from 'react';
import { View, Text, Alert, StyleSheet } from 'react-native';
import messaging from '@react-native-firebase/messaging';
import axios from 'axios';
import { API_BASE_URL } from './config';  // Asegúrate de tener este archivo de configuración

const App = () => {
  useEffect(() => {
    const requestPermission = async () => {
      const authStatus = await messaging().requestPermission();
      const isAuthorized =
        authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
        authStatus === messaging.AuthorizationStatus.PROVISIONAL;

      if (isAuthorized) {
        console.log('Notification permissions granted.');
        getTokenAndRegister();
      } else {
        console.log('Notification permissions denied.');
      }
    };

    const getTokenAndRegister = async () => {
      try {
        const token = await messaging().getToken();
        console.log('FCM Token:', token);
        await axios.post('https://localhost:8000/api/register-token/', {
          token,
        });
      } catch (error) {
        console.error('Error al obtener el token:', error);
      }
    };
    

    const unsubscribeForeground = messaging().onMessage(async remoteMessage => {
      console.log('Notification received in foreground:', remoteMessage);
      if (remoteMessage.notification) {
        Alert.alert(remoteMessage.notification.title || 'No Title', remoteMessage.notification.body || 'No Body');
      }
    });

    messaging().setBackgroundMessageHandler(async remoteMessage => {
      console.log('Notification received in background:', remoteMessage);
    });

    messaging().onTokenRefresh(token => {
      console.log('Token refreshed:', token);
      axios.post(`${API_BASE_URL}/register-token/`, { token }).catch(err => {
        console.error('Error updating token:', err);
      });
    });

    requestPermission();

    return () => {
      unsubscribeForeground();
    };
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.text}>React Native Notifications App</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    fontSize: 20,
    fontWeight: 'bold',
  },
});

export default App;
