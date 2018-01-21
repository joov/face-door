FILE=wpa_supplicant.conf
SRC_DIR="$UM_MOUNTPOINT"
DEST_DIR="/etc/wpa_supplicant"
if [[ -r "$SRC_DIR/$FILE" && -f "$SRC_DIR/$FILE" ]]; then
    cp "$SRC_DIR/$FILE" "$DEST_DIR"
    chmod 0600 "$DEST_DIR/$FILE"
    ifdown wlan0
    ifup wlan0
fi