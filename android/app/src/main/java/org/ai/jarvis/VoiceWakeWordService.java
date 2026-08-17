package org.ai.jarvis;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.widget.Toast;

import androidx.core.app.NotificationCompat;

public class VoiceWakeWordService extends Service {
    private SpeechRecognizer recognizer;
    private boolean listening = false;

    @Override public void onCreate() {
        super.onCreate();
        startForeground(1, new NotificationCompat.Builder(this, "jarvis")
                .setContentTitle("J.A.R.V.I.S.")
                .setContentText("Listening for JARVIS...")
                .setSmallIcon(R.drawable.icon)
                .build());
        startListening();
    }

    private void startListening() {
        if (recognizer == null || listening) return;
        recognizer = SpeechRecognizer.createSpeechRecognizer(this);
        recognizer.setRecognitionListener(new RecognitionListener() {
            @Override public void onReadyForSpeech(android.os.Bundle p1) {}
            @Override public void onBeginningOfSpeech() {}
            @Override public void onRmsChanged(float p1) {}
            @Override public void onBufferReceived(byte[] p1) {}
            @Override public void onEndOfSpeech() {
                startListening();
            }
            @Override public void onError(int p1) {
                startListening();
            }
            @Override public void onResults(android.os.Bundle results) {
                java.util.ArrayList<String> matches = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                if (matches != null) {
                    for (String text : matches) {
                        if (text != null && text.toLowerCase().contains("jarvis")) {
                            Intent i = new Intent(getApplicationContext(), MainActivity.class);
                            i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                            startActivity(i);
                            break;
                        }
                    }
                }
                startListening();
            }
            @Override public void onPartialResults(android.os.Bundle p1) {}
            @Override public void onEvent(int p1, android.os.Bundle p2) {}
        });
        Intent i = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        recognizer.startListening(i);
        listening = true;
    }

    @Override public int onStartCommand(Intent i, int flags, int startId) {
        return START_STICKY;
    }

    @Override public void onDestroy() {
        super.onDestroy();
        if (recognizer != null) { recognizer.destroy(); recognizer = null; }
    }

    @Override public IBinder onBind(Intent p1) { return null; }
}
