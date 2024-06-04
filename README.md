# Nutrition Logger v0.9
Track your meals through voicenotes.

## **First-Time Setup**
### <img src="https://www.svgrepo.com/show/354472/twilio-icon.svg" alt="Twilio Logo" height="15"> **Twilio Setup**
- [Create a free Twilio account.](https://www.twilio.com/try-twilio)

### **Tailscale Setup**
- [Create an account](https://login.tailscale.com/start).
- [Install Tailscale locally](https://login.tailscale.com/admin/machines).
- Install and start OpenSSH: (Ubuntu)
```bash
sudo apt install openssh-server
sudo systemctl start sshd
```

### <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub Logo" height="15"> **Codespace Setup**
- Open the [Twilio console](https://console.twilio.com/) and go to "Account Info".
- Open the [settings for Codespaces](https://github.com/settings/codespaces) and go to "Codespaces secrets".
- From the Twilio console, copy the "Account SID" and save it as `TWILIO_ACCOUNT_SID` in the secrets section.
- From the Twilio console, copy the "Auth Token" and save it as `TWILIO_AUTH_TOKEN` in the secrets section.
- (Linux) Save your username as `$LOCAL_USERNAME` in the secrets section.
  
**Note**: Don't forget to set repository access to `HC-85/Nutrition-Logger` for both secrets.

## **Usage**
- [Connect to the WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn).
- Send voice notes to the Twilio bot.
- Start the codespace:\
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/HC-85/Nutrition-Logger)

**Note**: State your meals starting with a quantity (eg. "150 grams of chicken", "one slice of pizza", etc.).

## Status
1. **Audio retrieval**
   - _Currently_: Voice notes are fetched via Twilio API sandbox.
2. **Audio to text**
   - _Currently_: Whisper (tiny) (large-v3 fails)
   - TODO: Fix large-v3 failure. (Probably storage)
3. **Text segmentation**:
   - _Currently_: GLiNER (large-v2.1)
   - TODO: Fine-tune to food-related labels.
4. **Vector encoding**:
   - _Currently_: SBERT (all-MiniLM-L6-v2)
   - TODO: Fine tune with food-related topics sentences.
5. **Data Querying**:
   - _Currently_: HNSW index from encoding English subset of columns `brand`+`prod_name`+`gen_name` of the [Open Food Facts dataset](https://huggingface.co/datasets/HC-85/open-food-facts/viewer/reduced).
   (See preprocessing/preprocess.py)
   - TODO: explore using separate indexes and weighting.
6. **Logging**:
   - _Currently_: item indices and timestamps are logged to a local SQLite database through Tailscale and sshfs.
7. **Log Inspection**:
   - _Currently_: script displays PrettyTable
   - TODO: Deploy visualization with a Phoenix webpage
8. **Reinforcement** - *pending*
   - TODO: Allow user to correct entries and use these corrections for reinforcement.

Other TODOs:
- Find smaller base image that works with the project (currently using universal).
