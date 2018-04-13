package com.ipromise

import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.widget.Toast
import com.google.gson.JsonObject
import com.ipromise.retrofit.ClientAPI
import kotlinx.android.synthetic.main.activity_main.*
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        btnREGISTER.setOnClickListener {
            val json = JsonObject()
            json.addProperty("username", username.text.toString())
            json.addProperty("password", password.text.toString())
            ClientAPI
                    .service
                    .getVectors(json)
                    .enqueue(object : Callback<ResponseBody> {
                        override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                            println("---TTTT :: POST Throwable EXCEPTION:: " + t.message)
                        }

                        override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                            if (response.isSuccessful) {
                                val msg = response.body()?.string()
                                println("---TTTT :: POST msg from server :: " + msg)
                                Toast.makeText(applicationContext, msg, Toast.LENGTH_SHORT).show()
                            }
                        }
                    })
        }

        btnLOGIN.setOnClickListener {
            val json = JsonObject()
            json.addProperty("username", username.text.toString())
            json.addProperty("password", password.text.toString())
            ClientAPI
                    .service
                    .getVectors2(json)
                    .enqueue(object : Callback<ResponseBody> {
                        override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                            println("---TTTT :: POST Throwable EXCEPTION:: " + t.message)
                        }

                        override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                            if (response.isSuccessful) {
                                val msg = response.body()?.string()
                                println("---TTTT :: POST msg from server :: " + msg)
                                Toast.makeText(applicationContext, msg, Toast.LENGTH_SHORT).show()
                            }
                        }
                    })
        }

    }
}
