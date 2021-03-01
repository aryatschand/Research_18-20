//
//  ViewController.swift
//  Research Interface
//
//  Created by AT on 12/31/19.
//  Copyright © 2020 at. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
    
    
    @IBAction func demo(_ sender: Any) {
        print("hit")
        
        let url = URL(string: "http://192.168.86.41:5000/?usage=giveDemo")!

        let task = URLSession.shared.dataTask(with: url) {(data, response, error) in
            guard let data = data else { return }
            print(String(data: data, encoding: .utf8)!)
        }

        task.resume()
        
    }
    

}

