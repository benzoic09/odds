<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class MainController extends Controller
{
    public function index(){
        // return ('this is index from main controller');
        return view('index');
    }

    
    public function about(){
        return ('this is about from main controller ');
    }
}
