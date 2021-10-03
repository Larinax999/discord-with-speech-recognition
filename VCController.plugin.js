/**
 * @name VCController
 * @author larinax999 (original by Eric Andrechek)
 * @description Opens a localhost API to control muting and deafening of your client.
 * @version 0.0.1
 * @authorLink https://github.com/larinax999
 * @donate https://paypal.me/AndrechekEric
 * @website https://github.com/EricAndrechek/VCController
 * @source https://github.com/EricAndrechek/VCController/raw/main/VCController.plugin.js
 */

const http = require("http");
const url = require('url');
module.exports = class VCController {
    start() {
		this.server = null;
        this.load();
		this.createServer();
    }
    stop() {
		this.server.close(()=>{console.log('Server closed!');});
	}
    load() {
		this.btn_mute = document.querySelector('[aria-label="Mute"]');
		this.btn_deaf = document.querySelector('[aria-label="Deafen"]');
		this.btn_screen = document.querySelector('[aria-label="Share Your Screen"]');
		this.btn_video = document.getElementsByClassName("button-38aScr lookFilled-1Gx00P colorBrand-3pXr91 sizeSmall-2cSMqn grow-q77ONN")[0];
    }
	press_btn(btn,tf,c=false) {
		if (btn != undefined) {
			if (btn.getAttribute("aria-checked") != tf || c) {
				btn.click();
			}
		}
	}
    createServer() {
        this.server = http.createServer((req, res) => {
            //let path = req.url.split("/")[1];
			const data = url.parse(req.url,true).query;
			//console.log(data);
			let do_ = data.do;
			let method = data.method;
            if (do_ == "mute") {
                res.writeHead(200, { "Content-Type": "text/plain" });
                res.end("Muting");
				this.press_btn(this.btn_mute,method);
            } else if (do_ == "deafen") {
                res.writeHead(200, { "Content-Type": "text/plain" });
                res.end("Deafening");
				this.press_btn(this.btn_deaf,method);
            } else if (do_ == "screen") {
                res.writeHead(200, { "Content-Type": "text/plain" });
                res.end("Starting/stopping stream");
				if (method == "true"){
					document.getElementsByClassName("button-38aScr lookFilled-1Gx00P colorBrand-3pXr91 sizeSmall-2cSMqn grow-q77ONN")[1].click();
					setTimeout(()=>{
						let a = document.getElementsByClassName("item-1TLUig segmentControlOption-1vCKaY")[1];
						if (a) {
							a.click();
							document.getElementsByClassName("tile-2w4k5N tile-8W93rZ")[0].click();
							document.getElementsByClassName("button-38aScr lookFilled-1Gx00P colorBrand-3pXr91 sizeSmall-2cSMqn grow-q77ONN")[2].click();
						}
					},1000);
				} else {
					let a = document.querySelector('[aria-label="Stop Streaming"]');
					if (a) {
						a.click();
					}
				}
            } else if (do_ == "video") {
                res.writeHead(200, { "Content-Type": "text/plain" });
                res.end("Starting/stopping video");
				this.press_btn(this.btn_video,true);
            } else if (do_ == "disconnect") {
                res.writeHead(200, { "Content-Type": "text/plain" });
                res.end("disconnecting");
				let a = document.querySelector('[aria-label="Disconnect"]');
				if (a) {
					a.click();
				}
            } else {
				res.writeHead(404, { "Content-Type": "text/plain" });
                res.end("do not found");
				return
			}
        });
        this.server.on("error", (err) => {});
        this.server.listen(3001, () => {});
    }
};
