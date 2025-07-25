{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.chromium
    pkgs.chromedriver
    pkgs.ffmpeg
    pkgs.curl
    pkgs.wget
  ];
}
