package com.ipromise.retrofit;

import com.google.gson.GsonBuilder
import com.google.gson.JsonObject
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*

class ClientAPI {

    interface APIService {
        @Headers("Authorization: $token")
        @GET("/users/")
        fun greetUser(token : String): Call<ResponseBody>

        @Headers("Content-type: application/json")
        @POST("/register")
        fun getVectors(@Body body: JsonObject): Call<ResponseBody>

        @POST("/login")
        fun getVectors2(@Body body: JsonObject): Call<ResponseBody>
    }

    companion object {
        private val retrofit = Retrofit.Builder()
                .baseUrl("http://10.0.2.2:5000")
                .addConverterFactory(GsonConverterFactory.create(GsonBuilder().create()))
                .build()

        var service = retrofit.create(APIService::class.java)
    }
}