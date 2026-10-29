import ImportList from "../imports/ImportList"
import Logo from "../Logo"
import Sidebar from "./Sidebar"
import axios from "axios"

const LeftSidebar = () => {
	const handleFileChange = async (e) => {
		const formData = new FormData();
		const selectedFile = e.target.files[0]
		formData.append(
			"myFile",
			selectedFile,
			selectedFile.name
		);
		const res = await axios.post("http://localhost:8000/upload", formData, {
			headers: {
				"Content-Type": "multipart/form-data",
			},
		})
		console.log(res.data)
	}

  return (
	<Sidebar>
		<div className="space-y-4">
			<Logo/>
			<div className="relative">
			<button className="btn bg-primary btn-sm w-full"> + Importer un document</button>
			<input type="file" onChange={handleFileChange}
				className="bg-transparent text-transparent absolute left-0 right-0 h-full w-full"/>
			</div>
			<ImportList/>
		</div>
	</Sidebar>
  )
}

export default LeftSidebar
