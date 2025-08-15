// import Vue from 'vue'

import {
    $,
    awesomplete,
    Moment,
    api_endpoints,
    validate,
    formValidate,
    helpers,
    store
} from "../../hooks.js";
export default {
    async fetchBooking(id){
        try {
            // 1. Send a request to the API endpoint and wait for the response
            // The endpoint URL is constructed using the provided 'id'
            const response = await fetch(api_endpoints.booking(id));

            // 2. Check for HTTP errors (e.g., 404 Not Found)
            if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }

            // 3. Parse the response body as JSON
            const bookingData = await response.json();

            // 4. Return the fetched data
            // The original code resolved with the entire 'response', but typically you want the data.
            // I'm returning the parsed data (bookingData) here.
            return bookingData; 

        } catch (error) {
            // Catch any network errors or errors thrown above
            console.error(`Failed to fetch booking with id ${id}:`, error);
            // Re-throw the error to allow for further error handling by the caller
            throw error;
        }
    }
}
