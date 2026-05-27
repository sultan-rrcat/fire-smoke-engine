import { BrowserRouter, Routes, Route } from "react-router-dom"
import UploadPage from "../pages/UploadPage"
import ProcessingPage from "../pages/ProcessingPage"
import ResultsPage from "../pages/ResultsPage"

export default function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<UploadPage />} />
                <Route path="/processing/:id" element={<ProcessingPage />} />
                <Route path="/results/:id" element={<ResultsPage />} />
            </Routes>
        </BrowserRouter>
    )
}