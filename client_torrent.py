import datetime
import libtorrent as lt
import time


def main():
    link = input("Paste your link here: ")

    ses = lt.session()
    ses.listen_on(6881, 6891)

    params = {
        'save_path': '/home/staval/Desktop/TBSDA/Lab_3/Download/',
        'storage_mode': lt.storage_mode_t(2)
    }

    print(link)

    handle = lt.add_magnet_uri(ses, link, params)
    ses.start_dht()

    begin = time.time()
    print(datetime.datetime.now())

    print("Downloading Metadata...")
    while(not handle.has_metadata()):
        time.sleep(1)

    print("Got Metadata, Start torrent downloading.")
    print("Starting", handle.name())

    while(handle.status().state != lt.torrent_status.seeding):
        s = handle.status()

        state_str = ["queued", "checking", "downloading metadata"\
            "downloading", "finished", "seeding", "allocating"]
        print("% .2f %% complete (down: %1f kb/s up: %.1f kb/s peers: %d) %s " % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, state_str[s.state]))

        time.sleep(5)

    end = time.time()
    print(handle.name(), " completed")
    print("Elapsed time: ", int((end - begin) // 60), "mins ", int((end - begin) % 60), "sec")
    print(datetime.datetime.now())
    


if __name__ == "__main__":
    main()
